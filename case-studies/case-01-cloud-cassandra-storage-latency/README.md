# Case Study 01 — Intermittent Cassandra Storage Latency in a Cloud Environment

> **Anonymized Engineering Case Study**
>
> This case study is based on a real production investigation conducted in a mission-critical enterprise environment.
>
> Organization names, infrastructure identifiers, exact capacity values, logs and business volumes have been removed or generalized.
>
> This document is an engineering reconstruction and does not represent an official statement from any organization or technology vendor.

---

## Executive Summary

A distributed API gateway platform experienced short and intermittent client-facing timeouts.

The events were difficult to reproduce because:

- They lasted only a few seconds at the database layer.
- They occurred at apparently random times.
- CPU and memory utilization remained within normal limits.
- Traffic volume did not consistently correlate with the incidents.
- The affected database node recovered automatically.

At the application layer, the brief degradation caused thread accumulation, connection redirection and autoscaling activity.

At the database layer, the events were associated with:

- Storage write-latency spikes
- Cassandra write timeouts
- Commit-log synchronization delays
- Dropped internal and cross-node messages
- Hints activity
- JVM pauses
- Temporary node unavailability

The investigation lasted several months and involved internal engineers, SREs and multiple technology vendors.

The decisive breakthrough was correlating short storage write-latency spikes with Cassandra write failures, hints activity, JVM pauses, node unavailability and gateway thread accumulation within the same observability window.

---

## Environment

The production environment included:

- A cloud-hosted API gateway platform
- Containerized gateway workloads
- Multiple gateway instances with automatic scaling
- Distributed Cassandra clusters
- Cassandra nodes distributed across availability zones
- A quorum-based consistency model
- Cloud-managed storage
- Enterprise observability and monitoring

Cassandra stored operational information required by the API gateway, including:

- API metadata
- Policies
- Quota-related information
- Tables and keyspaces used by gateway services

The gateway depended on Cassandra availability for critical request-processing operations.

---

## Business Impact

The incidents caused:

- Short-lived frontend timeouts
- Increased API latency
- Thread accumulation in gateway workloads
- Automatic connection redirection to healthy Cassandra nodes
- Temporary autoscaling activity
- A measurable but brief reduction in successful client activity

The database-layer degradation lasted seconds.

The client-facing impact could remain visible for one or two minutes while the platform recovered.

---

## Initial Symptoms

The investigation started with an unexpected increase in gateway worker threads.

The initial symptoms included:

- Gateway thread accumulation
- Autoscaling activity
- Cassandra write failures
- Read and write error metrics leaving their normal baseline
- JVM pause events
- Temporary Cassandra node degradation
- Short reductions in successful request volume

At first, the JVM and garbage collector appeared to be the likely cause.

Several JVM-related improvements were applied, but the incidents continued.

---

## Investigation Breakthrough

The investigation changed direction when observability data showed that the following events occurred in the same short time window:

```text
Storage write-latency spike
        ↓
Cassandra write timeout
        ↓
Commit-log and mutation delays
        ↓
Hints activity and additional I/O pressure
        ↓
JVM pause and node degradation
        ↓
Temporary node unavailability
        ↓
Gateway connection redirection
        ↓
Thread accumulation and client-facing timeouts

```
This evidence suggested that JVM pauses were more likely a symptom or secondary effect than the initiating failure.

---

## Root Cause Summary

The investigation identified transient storage-layer latency as the initiating failure mode.

The available evidence showed:

- Write operations were delayed.
- Commit-log synchronization exceeded expected intervals.
- Cassandra operations timed out.
- Internal and cross-node messages expired.
- One node became temporarily unavailable.
- Gateway workloads redirected connections and accumulated threads.

A cloud-provider root cause analysis later associated similar behavior with long flush operations caused by a limitation in a storage-virtualization component.

At the time of the customer-side remediation, the global platform fix had not yet been fully deployed.

The engineering team therefore implemented architectural improvements to reduce storage contention and increase I/O predictability.

---

## Remediation Summary

The storage architecture was changed from a shared, lower-tier layout to a more isolated and predictable design.

Main improvements included:

- Upgrading the Cassandra data disk to a higher-performance tier
- Increasing baseline IOPS and throughput
- Changing the redundancy model after evaluating latency and resilience trade-offs
- Creating a dedicated disk for the Cassandra commit log
- Separating SSTable and commit-log I/O patterns
- Changing host caching from Read/Write to None for latency-sensitive disks
- Automating the infrastructure changes using configuration management

The final storage layout separated:
```text
OS disk       → Operating system
Data disk     → Cassandra data and SSTables
Commit disk   → Cassandra commit log
Work disk     → Upgrades, temporary backups and operational files
```

---

## Result

After the architecture changes:

- Storage latency returned to the normal range of tens of milliseconds.
- Previously observed spikes in the hundreds of milliseconds were no longer detected.
- Cassandra nodes stopped becoming temporarily unavailable.
- Gateway error rates decreased.
- Observability data showed stable behavior.
- No similar incident was observed during the first month of monitoring.

The environment remained under observation because the cloud-provider platform fix was still being rolled out.

---

## SRE Contribution

The SRE work included:
- Designing the observability dashboards
- Defining infrastructure and application signals
- Correlating gateway, Cassandra, JVM, VM and disk metrics
- Identifying the decisive storage-latency relationship
- Collecting evidence across multiple incident windows
- Coordinating investigations with engineering teams and vendors
- Defining the storage architecture improvements
- Automating the remediation process
- Validating the environment after implementation

---

## Case Study Documents

- [Architecture](architecture.md)
- [Timeline](timeline.md)
- [Investigation](investigation.md)
- [Observability](observability.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Remediation](remediation.md)
- [Lessons Learned](lessons-learned.md)

---

## Key Engineering Lesson

Intermittent failures are rarely solved by analyzing a single layer.

The investigation required correlation across:
```text
Client behavior
        ↓
Gateway threads
        ↓
Container autoscaling
        ↓
Cassandra operations
        ↓
JVM behavior
        ↓
Operating system
        ↓
Cloud storage
        ↓
Virtualization platform
```

The most important lesson was:

Reliable troubleshooting requires understanding how application behavior interacts with the infrastructure beneath it.