# Investigation Timeline

This document reconstructs the investigation timeline at a generalized level.

Exact dates, times, ticket identifiers and internal environment names have been intentionally removed.

The investigation lasted several months because the events were brief, intermittent and difficult to reproduce.

---

## Timeline Overview

```text
Intermittent client-facing timeouts detected
        ↓
Gateway thread accumulation identified
        ↓
Cassandra write failures and JVM pauses observed
        ↓
Initial focus on JVM and garbage collection
        ↓
JVM and GC improvements applied
        ↓
Incidents continued
        ↓
Traffic, CPU, memory and scheduled jobs ruled out
        ↓
Cross-layer observability expanded
        ↓
Storage write-latency spikes correlated with failures
        ↓
Cassandra logs confirmed commit-log and mutation delays
        ↓
Vendor investigation expanded to cloud storage
        ↓
Cloud-provider RCA identified a storage-virtualization issue
        ↓
Storage architecture redesigned
        ↓
Changes automated and deployed
        ↓
Environment monitored with no recurrence during the initial observation period
```

---

## Phase 1 — Initial Symptoms

The investigation began when gateway workloads accumulated an abnormal number of processing threads.

At the same time, monitoring showed:

- Short-lived frontend timeouts
- A measurable reduction in successful client activity
- Cassandra write failures
- JVM pause events
- Gateway autoscaling activity

The incidents were brief.

At the Cassandra layer, the degradation often lasted only seconds.

At the client-facing layer, the impact remained visible for longer while the gateway recovered.

---

## Phase 2 — Initial JVM Hypothesis

The first major hypothesis was that the Cassandra JVM or garbage collector was causing the degradation.

The investigation identified prolonged JVM pauses and elevated garbage-collection duration around the incident windows.

Several improvements were applied:

- Runtime upgrade
- Garbage-collector change
- Garbage-collector tuning
- Heap-size adjustment

These changes improved the runtime configuration but did not eliminate the intermittent incidents.

This was the first indication that the JVM behavior might be a symptom rather than the initiating failure.

---

## Phase 3 — Workload and Infrastructure Saturation Ruled Out

The team analyzed whether the failures correlated with:

- High traffic
- Quota-processing volume
- CPU saturation
- Memory pressure
- Network saturation
- Backup jobs
- Cassandra repair operations
- Operating-system maintenance
- Scheduled batch processing

No consistent correlation was found.

The incidents occurred under both normal and low workload conditions.

CPU, memory and general VM utilization remained within expected ranges.

This evidence weakened the hypothesis that infrastructure saturation or application demand was the primary cause.

---

## Phase 4 — Observability Expansion

The SRE investigation expanded the monitoring scope to correlate signals across:

- Gateway workloads
- Gateway thread pools
- Autoscaling activity
- Cassandra services
- Cassandra read and write failures
- JVM and GC behavior
- Virtual-machine metrics
- Data-volume write latency
- Client activity

The dashboards aligned these signals within the same time window.

This was critical because the individual events were too short to diagnose using commands executed after recovery.

---

## Phase 5 — Storage Correlation Identified

A decisive pattern emerged.

Short storage write-latency spikes occurred at the same time as:

- Cassandra write timeouts
- JVM pauses
- Hints activity
- Commit-log delays
- Dropped internal messages
- Temporary node degradation
- Gateway thread accumulation

The decisive breakthrough was:

> The correlation of short storage write-latency spikes with Cassandra write failures, hints activity, JVM pauses, node unavailability and gateway thread accumulation within the same observability window.

The investigation focus shifted from the JVM to the storage path.

---

## Phase 6 — Cassandra Internals Analysis

Cassandra logs provided evidence of:

- Memtable flush operations
- Commit-log synchronization delays
- Mutation timeouts
- Dropped internal messages
- Dropped cross-node messages
- Temporary node-down events
- Automatic node recovery

The evidence suggested that one node became locally unresponsive before the other nodes reported communication failures.

This distinction was important.

The apparent network failure was actually a consequence of delayed local processing on the affected node.

---

## Phase 7 — Hints as an Amplifying Factor

The investigation observed hints activity around some incident windows.

The working model became:

```text
Storage latency
        ↓
Write acknowledgements delayed
        ↓
Write timeout
        ↓
Hints created
        ↓
Additional I/O pressure
        ↓
Higher storage contention
        ↓
Further Cassandra degradation
```

Hints were not treated as the original root cause.

They were considered a possible amplification mechanism after the storage degradation began.

---

## Phase 8 — Multi-Vendor Investigation

The investigation expanded across several engineering groups:

- Internal platform engineering
- Site Reliability Engineering
- API gateway specialists
- Database specialists
- Operating-system specialists
- Cloud-provider engineers

Multiple incident reviews and support cases were required.

The cloud platform initially appeared healthy when evaluated through standard infrastructure metrics.

The SRE team continued supplying:

- Timestamped correlations
- Cassandra logs
- VM metrics
- Storage-latency graphs
- Gateway impact evidence
- Repeated incident examples

The investigation remained open because the failures could not be explained by application load, VM saturation or network behavior alone.

---

## Phase 9 — Cloud Storage RCA

A formal cloud-provider investigation later associated the behavior with a limitation in a storage-virtualization component.

The provider identified that:

- A memory-allocation limit could affect a storage driver or virtualization component.
- The condition could generate long flush operations.
- Other I/O operations could be delayed while waiting for the flush to complete.
- A broader platform correction was being prepared.

At the time of the local remediation, the global platform fix had not yet been fully deployed.

The engineering team therefore proceeded with customer-side architectural improvements.

---

## Phase 10 — Storage Architecture Redesign

The remediation focused on reducing contention and improving latency predictability.

Changes included:

- Upgrading the data disk to a higher-performance tier
- Increasing baseline IOPS
- Increasing baseline throughput
- Moving from a shared data and commit-log path to separate disks
- Adding a dedicated commit-log disk
- Changing host caching from `Read/Write` to `None`
- Selecting a redundancy model based on workload latency requirements
- Automating the changes using configuration management

The objective was not merely to increase capacity.

The primary goal was to improve:

- Performance consistency
- Write-path isolation
- Latency predictability
- Operational repeatability

---

## Phase 11 — Deployment and Validation

The storage changes were deployed through controlled operational procedures.

After implementation, observability showed:

- Write latency returning to the normal range
- No recurrence of previous high-latency spikes
- No new temporary Cassandra node-down events
- Reduced gateway errors
- Stable thread behavior
- Stable client activity

The environment was monitored for approximately one month, and monitoring is still ongoing.

No similar incident was observed during that initial validation period.

---

## Representative Incident Window

The following timeline represents a generalized incident sequence.

Exact timestamps have been removed.

```text
T+00s
Storage write latency increases on one Cassandra node.

T+01s
Commit-log and mutation operations begin exceeding expected duration.

T+02s
Cassandra reports write timeouts.

T+03s
Hints activity and additional write pressure appear.

T+04s
Internal and cross-node messages begin to expire.

T+05s
Peer nodes temporarily mark the affected node as unavailable.

T+06s
Gateway connections are redirected to healthy Cassandra nodes.

T+10s
Gateway worker threads begin accumulating.

T+15s
Autoscaling reacts to thread pressure.

T+30s
The Cassandra node recovers automatically.

T+60–120s
Gateway queues, client requests and frontend activity return to normal.
```

This timeline is illustrative.

The exact duration varied between events, but the sequence remained consistent with the observed failure path.

---

## Why the Investigation Took Months

The investigation required months because:

- Events lasted only seconds.
- The affected node recovered automatically.
- Static diagnostics after the incident appeared normal.
- The issue occurred on different nodes over time.
- The incidents were not consistently load-driven.
- CPU and memory metrics appeared healthy.
- The symptoms initially suggested JVM or network problems.
- Multiple technology layers were involved.
- Standard cloud metrics did not immediately expose the platform-level issue.
- Vendor escalation required repeated evidence.

---

## Key Decision Points

## Decision 1 — Do Not Stop at the GC Symptom

The team continued investigating after applying JVM improvements.

## Decision 2 — Correlate Every Layer

The investigation aligned client, gateway, Cassandra, JVM, VM and disk signals.

## Decision 3 — Treat Storage as the Initiating Failure Mode

The storage write-latency pattern explained the downstream behavior better than the JVM-only hypothesis.

## Decision 4 — Reduce Architectural Contention

The team isolated commit-log I/O from Cassandra data operations.

## Decision 5 — Improve Predictability, Not Only Capacity

The remediation prioritized baseline performance and stable latency rather than burst performance alone.

---

## Related Documents

- [Case Overview](README.md)
- [Architecture](architecture.md)
- [Investigation](investigation.md)
- [Observability](observability.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Remediation](remediation.md)
- [Lessons Learned](lessons-learned.md)

---

## SRE Thinking

Intermittent incidents require timelines built from evidence.

A single metric rarely explains a distributed failure.

The investigation only advanced after every layer was aligned within the same time window:

```text
Storage
    ↓
Database
    ↓
JVM
    ↓
Gateway
    ↓
Autoscaling
    ↓
Client impact
```

Reliable incident timelines transform isolated symptoms into a defensible causal narrative.