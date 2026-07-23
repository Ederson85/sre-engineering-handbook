# Investigation

This document describes the investigation methodology, hypotheses, evidence and decision points used to diagnose the intermittent Cassandra degradation.

The incident required a cross-layer investigation because no single metric or log source explained the complete failure path.

---

## Investigation Objective

The investigation needed to answer five questions:

1. What initiated the incident?
2. Why did the Cassandra node become temporarily unavailable?
3. Why did the gateway accumulate threads even when most infrastructure metrics appeared healthy?
4. Why did the environment recover automatically before traditional diagnostics captured the failure?
5. Which engineering change could prevent recurrence?

---

## Investigation Principles

The investigation followed several SRE principles:

- Start from the user-visible symptom.
- Build a timeline before selecting a root cause.
- Separate initiating failures from downstream symptoms.
- Correlate application and infrastructure signals.
- Avoid treating temporal correlation as proof without supporting evidence.
- Preserve incident evidence before applying changes.
- Validate hypotheses across multiple occurrences.
- Prefer reversible and measurable remediation.

---

## Starting Point

The first visible technical signal was not a disk alert.

It was thread accumulation in the API gateway workloads.

```text
Client-facing timeout
        ↓
Gateway request remains pending
        ↓
Worker thread remains occupied
        ↓
Thread count increases
        ↓
Autoscaling reacts
```

This initially suggested several possible causes:

- Gateway processing degradation
- Backend service latency
- Cassandra response delay
- Network instability
- JVM pauses
- Resource saturation
- Storage latency

The investigation moved progressively through these layers.

---

## Hypothesis 1 — Gateway Capacity Problem

## Why It Was Considered

The gateway showed:

- Thread accumulation
- Increased response time
- Autoscaling activity
- Short-lived client-facing failures

This could indicate insufficient gateway capacity or a processing bottleneck.

## Evidence Reviewed

The team compared:

- Gateway instance count
- Thread activity
- CPU utilization
- Memory utilization
- Request volume
- Autoscaling behavior
- Backend response times

## Conclusion

Gateway workloads were reacting to downstream latency.

Adding instances helped absorb temporary pressure but did not eliminate the triggering event.

The gateway was not the initiating failure.

```text
Gateway scaling = recovery mechanism
Gateway thread accumulation = downstream symptom
```

---

## Hypothesis 2 — Traffic or Quota Volume

## Why It Was Considered

Cassandra stored metadata and quota-related information used by the gateway.

A traffic increase or quota-processing spike could increase database activity and produce timeouts.

## Evidence Reviewed

The investigation compared incident windows with:

- Request volume
- Successful client activity
- Quota usage
- Time of day
- Normal and low-load periods

## Conclusion

The incidents were not consistently associated with high traffic.

Similar workload levels frequently completed without degradation, while some incidents occurred under normal or low demand.

Traffic was therefore not considered the primary cause.

---

## Hypothesis 3 — CPU or Memory Saturation

## Why It Was Considered

High CPU, memory pressure or swapping could cause Cassandra and the JVM to become temporarily unresponsive.

## Evidence Reviewed

The SRE dashboards included:

- VM CPU utilization
- Memory utilization
- Load average
- Swap activity
- General infrastructure health
- Cassandra process behavior

## Conclusion

The VMs consistently remained within expected resource thresholds.

No repeatable correlation existed between the incidents and:

- CPU saturation
- Memory exhaustion
- Swap pressure
- General VM overload

Infrastructure saturation at the VM resource level was ruled out.

---

## Hypothesis 4 — JVM and Garbage Collection

## Why It Was Considered

The Cassandra logs showed elevated garbage-collection duration and JVM pauses around incident windows.

The apparent sequence initially looked like:

```text
Long GC pause
        ↓
Cassandra stops responding
        ↓
Write timeout
        ↓
Gateway impact
```

## Actions Taken

The runtime configuration was improved through:

- Java runtime upgrade
- Migration to a modern garbage collector
- Garbage-collector tuning
- Heap-size adjustment

## Evidence After the Changes

The incidents continued despite the JVM improvements.

The team also observed that:

- GC duration did not consistently correlate with workload.
- Similar traffic levels did not reproduce the pauses.
- Incidents occurred under low infrastructure utilization.
- Storage latency and write failures aligned with the same windows.

## Conclusion

The JVM behavior was real, but it did not adequately explain the initiating event.

The investigation reclassified GC from probable root cause to probable symptom or secondary effect.

```text
Original interpretation:
GC pause → Cassandra timeout

Revised interpretation:
Storage delay → Cassandra processing delay → JVM/GC pressure becomes visible
```

The available evidence did not prove that storage directly blocked the garbage collector.

It showed that both events occurred in the same failure window and that storage degradation better explained the broader sequence.

---

## Hypothesis 5 — Network Instability

## Why It Was Considered

Cassandra logs showed:

- Cross-node message failures
- Dropped messages
- A node marked temporarily unavailable
- Automatic reconnection

These symptoms could indicate an internode network problem.

## Evidence Reviewed

The analysis distinguished between:

- Messages delayed locally
- Messages expiring before transmission
- Cross-node messages timing out
- Peer nodes marking the affected node down
- Automatic recovery shortly afterward

## Key Finding

Some operations expired before reaching the network path.

The affected node first became locally unresponsive, and only afterward did peer nodes report communication failure.

## Conclusion

The network symptoms were downstream effects of node-level processing delay.

```text
Local node degradation
        ↓
Messages not processed in time
        ↓
Internode timeout
        ↓
Peers mark node unavailable
```

A network-only root cause did not explain the local commit-log, mutation and storage evidence.

---

## Hypothesis 6 — Scheduled Maintenance or Background Jobs

## Why It Was Considered

Cassandra maintenance and other background tasks can generate significant I/O.

Possible contributors included:

- Backups
- Repairs
- Compactions
- Large imports
- OS maintenance
- Batch jobs
- Platform changes

## Evidence Reviewed

The investigation checked operational calendars and workload activity around the incident windows.

## Conclusion

There was no consistent overlap with scheduled backups, repairs, operating-system maintenance or external batch jobs.

Compaction and flush activity existed as part of normal Cassandra operation, but no recurring scheduled activity explained all events.

Scheduled maintenance was ruled out as the primary cause.

---

## Hypothesis 7 — Cassandra Internal Write Path

## Why It Was Considered

The logs showed evidence associated with:

- Memtable flushes
- Commit-log synchronization
- Mutation processing
- Write timeouts
- Dropped messages
- Hints activity

This indicated that the failure path involved Cassandra write processing.

## Evidence Reviewed

The team examined time-aligned Cassandra events, including:

- A write operation exceeding its expected interval
- Commit-log synchronization delays
- Mutation timeout messages
- Internal and cross-node dropped messages
- Temporary node-down status
- Automatic node recovery

## Conclusion

Cassandra was directly affected, but its write path was waiting on a slower lower-level dependency.

The database behavior alone did not explain why the incidents were:

- Random
- Brief
- Present on different nodes over time
- Unrelated to CPU and memory saturation
- Temporally aligned with disk write latency

The Cassandra write path was the failure propagation layer, not necessarily the infrastructure root cause.

---

## Hypothesis 8 — Hints as the Root Cause

## Why It Was Considered

Hints activity appeared around some incident windows.

Hints introduce additional writes and could increase pressure on an already busy disk.

## Evidence Reviewed

The observability timeline showed a relationship between:

- Write-latency increase
- Write timeout
- Hints activity
- Additional local I/O
- Further degradation

## Conclusion

Hints were treated as an amplification mechanism.

They were likely created after write acknowledgements failed or timed out.

```text
Storage delay
        ↓
Write timeout
        ↓
Hints activity
        ↓
Additional I/O pressure
```

The investigation did not classify hints as the initiating root cause.

---

## Hypothesis 9 — Disk Burst Credit Exhaustion

## Why It Was Considered

The original disk tier supported credit-based bursting.

A sustained write workload could potentially exhaust burst credits and reduce performance to the baseline level.

This was especially relevant because Cassandra background operations can generate high write demand.

## Evidence Reviewed

The team evaluated:

- Disk tier characteristics
- Baseline IOPS
- Burst IOPS
- Throughput
- Write patterns
- Compaction and flush activity
- Cloud storage metrics

## Conclusion

Burst-credit exhaustion was technically plausible.

However, the available evidence did not conclusively demonstrate that credits had been exhausted during every incident.

The hypothesis remained a possible contributor, not the confirmed root cause.

This distinction was preserved in the final analysis.

---

## Hypothesis 10 — Storage-Layer Latency

## Why It Was Considered

The observability platform showed short write-latency spikes on the Cassandra data path.

These spikes aligned with:

- Cassandra write failures
- Commit-log delay
- Hints activity
- JVM pauses
- Temporary node unavailability
- Gateway thread accumulation
- Client-facing impact

## Cross-Layer Evidence

```text
Cloud disk metric
        ↓
Write latency increases

Cassandra metric
        ↓
Write failures leave baseline

Cassandra logs
        ↓
Commit-log and mutation delays

Cluster behavior
        ↓
Node temporarily marked unavailable

Gateway behavior
        ↓
Connections redirected and threads accumulate

Client behavior
        ↓
Short-lived timeouts and reduced successful activity
```

## Decisive Breakthrough

> The decisive breakthrough was correlating short storage write-latency spikes with Cassandra write failures, hints activity, JVM pauses, node unavailability and gateway thread accumulation within the same observability window.

## Conclusion

Transient storage write latency provided the most complete explanation for the observed failure path.

The investigation therefore treated storage latency as the initiating failure mode.

---

## Cross-Disk Correlation

An additional escalation signal was that separate managed disks could show latency degradation in the same event window.

This raised questions that could not be explained by a single filesystem or Cassandra directory.

The observation suggested investigation below the guest operating system, including:

- VM storage attachment
- Hypervisor behavior
- Storage virtualization
- Cloud platform internals

This evidence strengthened the case for cloud-provider escalation.

---

## Why Traditional Diagnostics Were Insufficient

Commands executed after the incident often showed a healthy environment.

Examples included:

```bash
nodetool status
nodetool tpstats
nodetool compactionstats
nodetool info
```

These commands remained useful, but the node had frequently recovered before they were executed.

The incidents were shorter than the response time required to:

1. Detect the issue.
2. Access the host.
3. Execute diagnostics.
4. Capture the degraded state.

Therefore, the investigation depended more heavily on:

- Persisted metrics
- Timestamped logs
- Event correlation
- Historical dashboards
- Repeated occurrence analysis

---

## Evidence Matrix

| Hypothesis | Supporting Evidence | Contradicting Evidence | Final Status |
|---|---|---|---|
| Gateway capacity | Thread accumulation and scaling | Gateway reacted to downstream latency | Symptom |
| Traffic spike | Cassandra depends on gateway workload | Incidents also occurred under normal or low load | Ruled out |
| CPU saturation | Could delay application processing | CPU remained within normal range | Ruled out |
| Memory pressure | Could trigger JVM instability | No consistent memory or swap pressure | Ruled out |
| JVM/GC | Long pauses were observed | JVM tuning did not eliminate incidents | Secondary symptom |
| Network failure | Internode messages timed out | Local processing failed before network transmission | Downstream symptom |
| Scheduled jobs | Could create I/O contention | No consistent operational overlap | Ruled out |
| Cassandra write path | Commit-log and mutation delays confirmed | Lower-level storage delay better explained initiation | Propagation layer |
| Hints | Added write pressure | Appeared after write degradation began | Amplifier |
| Burst credits | Technically plausible | Not conclusively demonstrated | Possible contributor |
| Storage latency | Aligned with every major downstream signal | No stronger alternative explained the full chain | Initiating failure mode |
| Storage virtualization | Provider RCA identified platform behavior | Global fix not yet deployed during local remediation | Platform-level cause |

---

## Vendor Collaboration

The investigation required collaboration among:

- Internal SREs
- Platform engineers
- API gateway specialists
- Database specialists
- Operating-system specialists
- Cloud-provider engineers

The internal team supplied:

- Sanitized incident timelines
- Storage-latency evidence
- Cassandra logs
- JVM evidence
- Gateway impact metrics
- Multiple examples from separate incident windows
- Results of previously applied mitigations

The vendors contributed:

- Product-specific analysis
- Cassandra configuration recommendations
- Runtime recommendations
- Storage architecture recommendations
- Cloud platform investigation
- Provider-level root cause analysis

---

## Investigation Outcome

The investigation produced three separate conclusions.

## Initiating Failure Mode

Transient storage write latency.

## Failure Propagation

```text
Storage delay
→ Cassandra write-path delay
→ node degradation
→ gateway backpressure
→ client-facing impact
```

## Platform-Level Cause

A provider investigation associated the behavior with long flush operations in a storage-virtualization component.

---

## What Made the Investigation Successful

The investigation succeeded because the team:

- Continued after the first plausible explanation.
- Did not treat GC as proven root cause.
- Collected evidence across repeated events.
- Aligned every signal to the same time window.
- Distinguished local processing failure from network symptoms.
- Separated root cause, propagation and amplification.
- Escalated with defensible evidence.
- Implemented remediation that could be measured afterward.

---

## Related Documents

- [Case Overview](README.md)
- [Architecture](architecture.md)
- [Timeline](timeline.md)
- [Observability](observability.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Remediation](remediation.md)
- [Lessons Learned](lessons-learned.md)

---

## SRE Thinking

The first plausible explanation is not always the correct one.

In this case:

```text
GC looked like the cause.
Network errors looked like the cause.
Cassandra looked like the cause.
```

Each was real, but each represented a different part of the failure chain.

The investigation only reached the initiating failure by moving downward through every dependency until the evidence formed one consistent timeline.