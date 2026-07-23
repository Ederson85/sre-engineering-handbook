# Root Cause Analysis

This document presents the technical root cause analysis for the intermittent Cassandra degradation.

The analysis separates:

- Initiating failure
- Failure propagation
- Amplifying factors
- Contributing conditions
- Platform-level cause
- Evidence confidence

This separation is important because several symptoms appeared at the same time, but they did not all represent the original cause.

---

## Executive RCA Summary

The incident was initiated by transient write-latency degradation in the cloud storage path used by Cassandra.

The storage delay affected Cassandra write processing, especially operations associated with:

- Commit-log synchronization
- Mutations
- Memtable flushes
- Hints
- Cross-node acknowledgement timing

As write operations exceeded expected timing, Cassandra reported write timeouts and dropped messages.

The affected node became temporarily unavailable to its peers.

Gateway workloads redirected connections, accumulated worker threads and triggered autoscaling.

The user-visible impact persisted longer than the original storage event because downstream queues and active requests required time to recover.

A formal cloud-provider investigation later associated similar behavior with long flush operations caused by a limitation in a storage-virtualization component.

At the time of the local remediation, the global provider correction had not yet been fully deployed.

The engineering team therefore reduced exposure through storage isolation, higher baseline performance and host-caching changes.

---

## Root Cause Model

```text
Platform-Level Storage Virtualization Condition
                        ↓
Transient Storage Write-Latency Spike
                        ↓
Cassandra Write-Path Delay
                        ↓
WriteTimeoutException and Commit-Log Delay
                        ↓
Dropped Messages and Temporary Node Degradation
                        ↓
Gateway Connection Redirection
                        ↓
Thread Accumulation and Autoscaling
                        ↓
Short-Lived Client-Facing Timeouts
```

---

## Initiating Failure

## Definition

The initiating failure was the first observable technical condition that best explained the downstream event sequence.

## Identified Initiating Failure

> Transient write-latency degradation in the cloud-managed storage path used by Cassandra.

## Supporting Evidence

The following signals aligned within the same incident window:

- Data-volume write latency increased sharply.
- Cassandra write-failure metrics left their baseline.
- Commit-log synchronization was delayed.
- Mutation processing exceeded expected duration.
- Internal messages expired.
- Cross-node messages were dropped.
- The affected node became temporarily unavailable.
- Gateway threads accumulated.
- Client-facing timeouts appeared.

## Why It Was Classified as the Initiating Failure

Storage latency appeared before or at the beginning of the Cassandra failure window.

It also explained a broader set of downstream symptoms than any competing hypothesis.

---

## Failure Propagation

The storage event propagated through multiple layers.

## Layer 1 — Storage

```text
Write operation delayed
```

The managed disk temporarily required significantly longer to complete writes.

---

## Layer 2 — Cassandra Write Path

```text
Storage delay
        ↓
Commit-log synchronization delay
        ↓
Mutation processing delay
        ↓
Write timeout
```

Cassandra depends on timely storage acknowledgement for critical write-path operations.

When write completion was delayed, requests exceeded configured timeouts.

---

## Layer 3 — Cassandra Cluster

```text
Local node processing delay
        ↓
Messages expire
        ↓
Peer nodes receive no timely response
        ↓
Affected node marked temporarily unavailable
```

The cluster interpreted the slow node as unavailable because required responses did not arrive within expected timing.

---

## Layer 4 — Gateway

```text
Cassandra operation delayed
        ↓
Gateway request remains pending
        ↓
Worker thread remains occupied
        ↓
Thread count increases
        ↓
Connections redirect to healthy nodes
```

The gateway was resilient enough to redirect connectivity, but requests already in progress continued consuming resources.

---

## Layer 5 — Autoscaling

```text
Thread pressure increases
        ↓
Autoscaling trigger activates
        ↓
Additional gateway instances start
```

Autoscaling helped absorb pressure but occurred after the initiating event.

It was a recovery mechanism rather than a root cause.

---

## Layer 6 — Client Impact

```text
Gateway queueing and backend delay
        ↓
Frontend timeout threshold exceeded
        ↓
Short-lived client-facing failure
```

The original storage event lasted seconds.

The visible service impact lasted longer because the platform needed time to drain accumulated work.

---

## Amplifying Factors

Amplifying factors did not initiate the incident, but they increased its duration or impact.

---

## Hints Activity

When write acknowledgements failed or timed out, Cassandra could generate hints.

```text
Write timeout
        ↓
Hints created
        ↓
Additional local writes
        ↓
Higher I/O pressure
```

Hints were therefore treated as an amplification mechanism.

They were not classified as the original root cause.

---

## Shared Data and Commit-Log Path

The initial architecture placed several write-intensive Cassandra activities on the same data disk.

These included:

- SSTable writes
- Memtable flushes
- Compactions
- Commit-log synchronization
- Hints activity

This increased the possibility of contention during transient storage degradation.

---

## Quorum Sensitivity

Critical operations used a local quorum consistency model.

A slow replica could therefore delay or prevent successful completion within the configured timeout.

The quorum model was not incorrect.

However, it made node-level latency directly relevant to request success.

---

## Short Frontend Timeout

The frontend used a relatively short timeout.

This improved failure responsiveness but reduced tolerance for brief backend degradation.

The timeout did not cause the incident, but it made the user-visible impact appear quickly.

---

## Gateway Thread Retention

Requests waiting on Cassandra continued occupying gateway worker threads.

This produced:

- Thread accumulation
- Temporary backpressure
- Autoscaling activity
- Recovery delay after Cassandra returned

---

## Contributing Conditions

Contributing conditions increased exposure but were not independently proven as root cause.

---

## Mid-Tier Storage Baseline

The original data disk used a lower baseline than the final design.

The workload depended more heavily on the behavior of:

- Baseline IOPS
- Baseline throughput
- Credit-based bursting
- Shared write patterns

This reduced performance predictability for a latency-sensitive database workload.

---

## Credit-Based Bursting

Burst-credit exhaustion was investigated as a possible contributor.

The disk tier supported credit-based bursting, and Cassandra background operations could generate sustained write demand.

However, the available evidence did not conclusively prove that burst credits were exhausted during every incident.

Final classification:

```text
Possible contributor
Not confirmed root cause
```

---

## Host Caching

The initial configuration used `Read/Write` host caching.

For the latency-sensitive Cassandra data path, this added another layer of behavior between the application and managed storage.

The remediation changed caching to `None`.

The investigation did not independently prove that caching caused the incidents.

It was treated as a design factor worth removing from the critical write path.

---

## Redundancy and Latency Trade-Off

The original design prioritized zone-level storage resilience.

The final design used a different redundancy model for latency-sensitive paths after evaluating workload requirements.

This does not imply that one storage redundancy model is universally superior.

The relevant engineering question was:

> Which design provided the appropriate balance of durability, availability and latency predictability for this workload?

---

## JVM and Garbage Collection Classification

## Observed Behavior

The incident windows included:

- Increased GC duration
- Long JVM pauses
- Temporary Cassandra responsiveness degradation

## Initial Interpretation

The JVM was initially considered the most likely root cause.

## Evidence Against JVM as Initiating Cause

- Runtime and collector improvements did not eliminate the incident.
- Incidents occurred under normal and low load.
- CPU and memory remained within expected ranges.
- Storage write latency aligned with the same failure window.
- Storage degradation better explained commit-log and mutation delays.

## Final Classification

```text
JVM pauses = confirmed symptom or secondary effect
Direct storage-to-GC blocking = not conclusively proven
GC as initiating root cause = rejected
```

---

## Network Classification

## Observed Behavior

- Internode messages timed out.
- Peer nodes marked one member unavailable.
- Connections were later restored.

## Why Network Was Not Classified as Root Cause

Evidence indicated that some operations expired before reaching the network path.

The affected node became locally unresponsive first.

Peer communication failures appeared afterward.

## Final Classification

```text
Network errors = downstream symptom
Network-only root cause = rejected
```

---

## Cassandra Classification

Cassandra was the primary propagation layer.

It exposed the failure through:

- WriteTimeoutException
- Commit-log delay
- Mutation delay
- Dropped messages
- Temporary node unavailability
- Hints activity

However, Cassandra alone did not explain:

- Why events were random
- Why different nodes could be affected
- Why CPU and memory remained healthy
- Why storage latency aligned with failures
- Why separate disks could degrade within the same window

Final classification:

```text
Cassandra = affected system and propagation layer
Cassandra configuration alone = insufficient root-cause explanation
```

---

## Platform-Level RCA

A formal cloud-provider investigation associated the behavior with a limitation in a storage-virtualization component.

The provider described a condition in which:

- A memory-allocation limit affected a storage-related component.
- Long flush operations could occur.
- Other I/O operations could remain delayed while the flush completed.
- A broader platform correction was planned.

This provider finding explained why the issue:

- Appeared below the guest operating system
- Was intermittent
- Could affect different VMs over time
- Was difficult to reproduce
- Was not visible as traditional CPU or memory saturation
- Could influence more than one attached disk in the same event window

The original provider communication is confidential and is not reproduced in this case study.

---

## Evidence Confidence

## High Confidence

The following conclusions were directly supported by correlated metrics and logs:

- Storage write latency increased during incident windows.
- Cassandra write operations timed out.
- Commit-log synchronization was delayed.
- Messages were dropped.
- A node became temporarily unavailable.
- Gateway threads accumulated.
- Client-facing timeouts occurred.
- No similar event recurred during the initial post-remediation observation period.

---

## Medium-to-High Confidence

The following conclusions were strongly supported but involved interpretation across layers:

- Storage latency was the initiating failure mode.
- Hints increased I/O pressure after write degradation began.
- JVM pauses were secondary to the broader event.
- Gateway scaling was a downstream recovery response.
- Shared data and commit-log I/O increased contention risk.

---

## Medium Confidence

The following remained plausible contributors:

- Credit-based bursting behavior
- Host-caching behavior
- Redundancy-model latency characteristics

These factors influenced the remediation design but were not independently proven as the sole cause.

---

## Provider-Confirmed

The cloud provider formally associated the behavior with long flush operations in the storage-virtualization layer.

Because the platform fix had not yet been fully deployed at the time of local remediation, the team could not validate the provider correction directly.

The provider RCA was therefore treated as authoritative platform evidence, while the customer-side validation focused on the local architectural changes.

---

## Root Cause Statement

> A transient cloud storage write-latency condition delayed Cassandra commit-log and mutation processing. This caused write timeouts, dropped messages and temporary node unavailability. The degradation propagated into the API gateway through connection redirection, worker-thread accumulation and autoscaling, producing short-lived client-facing timeouts. A cloud-provider RCA later associated the underlying storage behavior with long flush operations in a storage-virtualization component.

---

## Contributing-Factor Statement

> The initial storage design increased exposure by combining Cassandra data and commit-log I/O on a shared mid-tier disk, relying on variable burst behavior and using host caching on latency-sensitive paths.

---

## Why the Remediation Was Valid

The remediation addressed the observed failure path by:

- Increasing baseline IOPS
- Increasing baseline throughput
- Reducing dependency on burst behavior
- Isolating commit-log writes
- Separating data and operational I/O patterns
- Disabling host caching on latency-sensitive disks
- Selecting a storage redundancy model aligned with workload requirements

The environment was then observed for approximately one month with no recurrence of the previous failure pattern. Note: monitoring of the environment is ongoing.

This does not prove that every architectural change was independently necessary.

It demonstrates that the combined remediation reduced exposure to the identified failure mode.

---

## Five Whys

## 1. Why did clients experience timeouts?

Because gateway requests waited too long for backend completion.

## 2. Why did gateway requests wait?

Because Cassandra operations were delayed and gateway threads remained occupied.

## 3. Why were Cassandra operations delayed?

Because commit-log and mutation writes exceeded expected duration.

## 4. Why did write operations exceed expected duration?

Because the storage path experienced transient write-latency degradation.

## 5. Why did the storage path degrade?

A provider RCA associated the behavior with long flush operations caused by a limitation in the storage-virtualization layer.

---

## Root Cause vs. Symptom Matrix

| Signal | Classification |
|---|---|
| Client timeout | User-visible symptom |
| Gateway thread accumulation | Downstream symptom |
| Autoscaling | Recovery mechanism |
| Cassandra write timeout | Database symptom |
| Dropped internode messages | Propagation symptom |
| Temporary node-down event | Cluster symptom |
| Hints activity | Amplifier |
| JVM pause | Secondary symptom |
| Write-latency spike | Initiating failure mode |
| Storage-virtualization flush condition | Platform-level cause |

---

## What Was Not Proven

The investigation did not conclusively prove that:

- Garbage collection initiated the event.
- A network fault initiated the event.
- Burst credits were exhausted during every incident.
- Hints created the original storage problem.
- ZRS is universally slower than LRS.
- Host caching alone caused the incident.
- Every individual remediation step was independently required.

Preserving these boundaries increases the credibility of the RCA.

---

## Related Documents

- [Case Overview](README.md)
- [Architecture](architecture.md)
- [Timeline](timeline.md)
- [Investigation](investigation.md)
- [Observability](observability.md)
- [Remediation](remediation.md)
- [Lessons Learned](lessons-learned.md)

---

## SRE Thinking

A strong RCA does not force every observation into a single label.

It separates:

```text
Root cause
Propagation
Amplification
Symptoms
Recovery mechanisms
Contributing factors
```

In this incident, several systems behaved incorrectly at the same time.

The engineering challenge was determining which behavior started the chain and which behaviors occurred because the chain had already started.