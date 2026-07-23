# Observability

This document describes how observability transformed a brief and intermittent production failure into a measurable cross-layer incident.

The investigation could not rely on a single dashboard, metric or log source.

The decisive evidence came from correlating signals across the client, gateway, Cassandra, JVM, virtual-machine and storage layers within the same time window.

---

## Observability Objective

The observability strategy needed to answer four questions:

1. When did the degradation begin?
2. Which technical layer showed the first abnormal signal?
3. How did the failure propagate through the platform?
4. How could recovery be validated after remediation?

---

## Why Observability Was Critical

The incidents were difficult to capture because:

- The storage degradation lasted only seconds.
- The affected Cassandra node recovered automatically.
- Gateway recovery took longer than the original storage event.
- Commands executed after the incident often showed a healthy environment.
- The events did not consistently correlate with high load.
- Different nodes could be affected over time.

Traditional point-in-time troubleshooting was insufficient.

The investigation required persisted telemetry with synchronized timestamps.

---

## Observability Layers

The monitoring model included the following layers:

```text
Client Activity
        ↓
Frontend Services
        ↓
API Gateway Workloads
        ↓
Gateway Thread Pools
        ↓
Autoscaling
        ↓
Cassandra Service
        ↓
JVM and Garbage Collection
        ↓
Virtual Machine
        ↓
Managed Disks
```

Each layer produced a different symptom of the same event.

---

## Client and Business Signals

The highest-level indicators showed the effect experienced by consumers.

Signals included:

- Successful client activity
- Request completion
- Frontend timeouts
- Short-lived reduction in successful operations
- Recovery duration

The business-facing degradation remained visible longer than the initiating storage event.

```text
Storage event: seconds

Client-visible impact: approximately one or two minutes
```

This difference demonstrated that downstream queues and threads required time to drain after the database recovered.

---

## Gateway Signals

The gateway layer showed:

- Worker-thread accumulation
- Requests remaining active longer than expected
- Backend response delay
- Temporary failure increase
- Automatic connection redirection
- Autoscaling activity

The gateway thread count was one of the first operational symptoms that triggered the investigation.

```text
Cassandra response delayed
        ↓
Gateway request remains pending
        ↓
Worker thread remains occupied
        ↓
Thread count increases
        ↓
Autoscaling reacts
```

The scaling mechanism helped the gateway absorb pressure, but it did not remove the underlying database dependency.

---

## Autoscaling Signals

The environment used thread pressure as an autoscaling signal.

The monitoring strategy correlated:

- Current gateway instance count
- Thread count
- Scaling trigger activation
- Scaling events
- Time required to return to the baseline

Exact internal scaling thresholds were intentionally removed from this case study.

The important observation was that autoscaling occurred after the Cassandra degradation had already begun.

```text
Storage latency
        ↓
Database delay
        ↓
Gateway thread pressure
        ↓
Autoscaling
```

Autoscaling was therefore classified as a recovery mechanism, not the root cause.

---

## Cassandra Service Signals

The observability platform monitored Cassandra service behavior, including:

- Read failures
- Write failures
- Request latency
- Node responsiveness
- Service failure events
- Error-rate deviation from baseline

During incident windows, read and write failure metrics left their expected baseline.

The strongest signal was the increase in write failures aligned with storage write latency.

---

## Cassandra Internal Signals

Application logs and internal metrics added evidence that infrastructure dashboards alone could not provide.

Relevant signals included:

- `WriteTimeoutException`
- Commit-log synchronization duration
- Mutation-processing delay
- Dropped internal messages
- Dropped cross-node messages
- Hints activity
- Memtable flush operations
- Temporary node-down events
- Automatic node recovery

These signals helped reconstruct the sequence inside Cassandra.

```text
Write operation delayed
        ↓
Commit-log synchronization delayed
        ↓
Mutation timeout
        ↓
Messages expire
        ↓
Node temporarily marked unavailable
```

---

## JVM and Garbage-Collection Signals

The investigation monitored:

- Garbage-collection duration
- Long JVM pauses
- Heap behavior
- Runtime stability
- Correlation with traffic and infrastructure load

At first, elevated GC duration appeared to be the probable cause.

After JVM improvements were applied, the incidents continued.

The observability timeline showed that JVM pauses occurred in the same window as storage and Cassandra write-path degradation.

This changed the interpretation from:

```text
GC causes Cassandra failure
```

to:

```text
Storage degradation initiates the event
        ↓
Cassandra processing is delayed
        ↓
JVM and GC pressure become visible
```

The evidence supported correlation, but not the claim that storage directly blocked the garbage collector.

---

## Virtual-Machine Signals

VM dashboards included:

- CPU utilization
- Memory utilization
- Load average
- General process health
- Disk activity
- Network behavior
- Operating-system availability

These metrics were important for ruling out common explanations.

During the incidents:

- CPU remained within expected limits.
- Memory remained within expected limits.
- No consistent resource saturation appeared.
- The VM remained generally available.
- The database process became temporarily degraded.

This helped narrow the investigation toward the storage path rather than general VM exhaustion.

---

## Storage Signals

The storage dashboards included:

- Write latency
- Read latency
- Disk utilization
- IOPS
- Throughput
- Queue behavior
- Data-volume health
- Latency deviation from baseline

The decisive metric was write latency on the Cassandra data volume.

Under normal conditions, latency remained in the range of tens of milliseconds.

During incidents, short spikes reached the range of hundreds of milliseconds.

Exact values were generalized to protect internal infrastructure details.

---

## Critical Correlation

The decisive observability window aligned the following signals:

```text
Storage write latency increases
        ↓
Cassandra write failures leave baseline
        ↓
Commit-log synchronization is delayed
        ↓
Hints activity appears
        ↓
JVM pause duration increases
        ↓
Cassandra node becomes temporarily unavailable
        ↓
Gateway connections are redirected
        ↓
Gateway threads accumulate
        ↓
Autoscaling activates
        ↓
Client-facing timeouts become visible
```

No individual signal proved the complete root cause.

Together, they formed a consistent propagation path.

---

## Time Alignment

The dashboards used the same incident window to compare:

- Disk write latency
- Cassandra failures
- JVM pauses
- Node availability
- Gateway threads
- Autoscaling events
- Client activity

Time alignment was essential because the events occurred too quickly for manual diagnostics.

A representative pattern was:

```text
T+00s
Storage write latency increases.

T+01s
Cassandra write processing slows.

T+02s
Write failures and commit-log delays appear.

T+03s
Hints and dropped-message activity increase.

T+05s
Node becomes temporarily unavailable.

T+06s
Gateway redirects connections.

T+10s
Gateway threads accumulate.

T+15s
Autoscaling activates.

T+30s
Cassandra node recovers.

T+60–120s
Client-facing activity returns to normal.
```

This sequence is illustrative and does not expose exact production timestamps.

---

## Baselines

Static thresholds alone were not sufficient.

The investigation used baseline deviation to identify abnormal behavior.

Relevant examples included:

- Cassandra write failures leaving the normal baseline
- Storage latency moving far above the normal range
- Gateway threads increasing beyond expected behavior
- Client activity dropping outside normal variation

Baselines helped distinguish:

```text
Normal operational variation
```

from:

```text
Short abnormal production degradation
```

---

## Dashboards

The SRE dashboards grouped signals by investigation purpose.

## Platform Health View

Included:

- VM CPU
- VM memory
- Load average
- Disk health
- General infrastructure status

Purpose:

- Rule out broad infrastructure saturation
- Confirm host responsiveness
- Compare affected and healthy nodes

---

## Cassandra Health View

Included:

- Read failure rate
- Write failure rate
- Request latency
- Node health
- JVM pauses
- Cassandra process behavior

Purpose:

- Detect database degradation
- Compare node behavior
- Correlate JVM and Cassandra signals

---

## Storage Investigation View

Included:

- Data-volume write latency
- Read latency
- IOPS
- Throughput
- Disk utilization
- Queue behavior
- Cross-disk comparison

Purpose:

- Identify storage as the initiating layer
- Compare latency across separate managed disks
- Validate behavior before and after remediation

---

## Gateway Impact View

Included:

- Gateway response time
- Worker threads
- Failure rate
- Instance count
- Autoscaling events
- Backend dependency behavior

Purpose:

- Measure propagation into the application layer
- Distinguish downstream symptoms from initiating causes

---

## Client Impact View

Included:

- Successful client activity
- Timeout behavior
- Short-term request degradation
- Recovery time

Purpose:

- Quantify user-visible impact
- Confirm end-to-end recovery

---

## Suggested SLI Model

The case led to a clearer SLI structure across the platform.

## Storage SLIs

- Write latency
- Read latency
- IOPS utilization
- Throughput utilization
- Queue depth or equivalent queue signal
- Burst-credit state when applicable

## Cassandra SLIs

- Write success rate
- Read success rate
- Write latency
- Read latency
- Node availability
- Dropped messages
- Commit-log synchronization duration
- JVM pause duration

## Gateway SLIs

- Request success rate
- Request latency
- Worker-thread utilization
- Backend dependency latency
- Autoscaling frequency
- Queue recovery time

## Client SLIs

- Successful operation rate
- Timeout rate
- End-to-end latency
- Recovery duration

---

## Alerting Strategy

A single storage-latency alert would not fully represent the incident.

A stronger strategy combines multiple conditions.

## Early Warning

Possible signals:

- Storage write latency above baseline
- Commit-log synchronization delay
- Cassandra write failures
- Increased dropped messages

## Service Degradation

Possible signals:

- Temporary node unavailability
- Gateway thread accumulation
- Backend request latency
- Autoscaling activation

## User Impact

Possible signals:

- Frontend timeouts
- Reduced successful client activity
- Request success-rate degradation

---

## Composite Incident Signal

A useful incident model would be:

```text
Storage latency abnormal
AND
Cassandra write failures abnormal
AND
Gateway thread pressure increasing
```

This correlation is more meaningful than any isolated alert.

It reduces the risk of:

- Alerting on harmless storage variation
- Treating gateway scaling as the root cause
- Investigating JVM pauses without lower-layer context

---

## Evidence Preservation

For short incidents, evidence must be retained automatically.

The investigation benefited from:

- Persisted metrics
- Historical dashboard windows
- Timestamped logs
- Event markers
- Baseline comparisons
- Cross-layer correlation

Recommended evidence to preserve includes:

- Incident start and end time
- Affected node
- Disk write-latency window
- Cassandra write-failure window
- Commit-log events
- JVM pause events
- Gateway thread behavior
- Autoscaling behavior
- Client-impact duration

---

## Before and After Validation

Observability was also used to validate remediation.

## Before

Observed behavior included:

- Write-latency spikes in the hundreds of milliseconds
- Cassandra write failures
- Temporary node unavailability
- Gateway thread accumulation
- Short-lived client impact

## After

During the initial observation period:

- Write latency remained in the normal range
- Previous high-latency spikes were not observed
- Cassandra nodes remained responsive
- Gateway errors decreased
- Thread behavior stabilized
- No similar incident recurred

The environment was monitored for approximately one month after the architecture changes.

---

## Observability Anti-Patterns Avoided

## Single-Layer Monitoring

Looking only at gateway metrics would have suggested a capacity problem.

## JVM-Only Analysis

Looking only at GC logs would have suggested a garbage-collection root cause.

## Infrastructure-Only Analysis

Looking only at CPU and memory would have suggested the environment was healthy.

## Snapshot Diagnostics

Running commands after recovery would have missed the degraded state.

## Single Threshold Alerting

A single fixed threshold would not have explained the failure path.

---

## What Made the Observability Effective

The observability model worked because it:

- Started from the client-visible symptom.
- Included every dependency layer.
- Preserved short-lived events.
- Used synchronized time windows.
- Compared signals against baselines.
- Distinguished initiation from propagation.
- Supported vendor escalation with evidence.
- Validated the remediation afterward.

---

## Related Documents

- [Case Overview](README.md)
- [Architecture](architecture.md)
- [Timeline](timeline.md)
- [Investigation](investigation.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Remediation](remediation.md)
- [Lessons Learned](lessons-learned.md)

---

## SRE Thinking

Monitoring shows whether a component is healthy.

Observability helps explain why the system behaved the way it did.

In this incident, the answer was not inside one metric.

It existed in the relationship between:

```text
Storage latency
Cassandra write behavior
JVM pauses
Node availability
Gateway threads
Autoscaling
Client impact
```

The decisive engineering capability was not collecting more data.

It was aligning the right signals within the same failure window.