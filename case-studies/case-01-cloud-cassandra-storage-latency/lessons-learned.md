# Lessons Learned

This document consolidates the technical, operational and organizational lessons learned during the investigation and remediation of intermittent Cassandra storage latency.

The most important lesson was that the incident could not be understood from a single technology layer.

It required correlation across:

```text
Client behavior
        ↓
Gateway threads
        ↓
Autoscaling
        ↓
Cassandra operations
        ↓
JVM behavior
        ↓
Virtual machine
        ↓
Cloud storage
        ↓
Storage virtualization
```

---

## 1. Symptoms and Root Causes Must Be Separated

Several real technical problems appeared during the incident:

- JVM pauses
- Cassandra write timeouts
- Dropped messages
- Temporary node unavailability
- Gateway thread accumulation
- Autoscaling activity
- Client-facing timeouts

Every one of these signals was valid.

However, they represented different stages of the same failure chain.

The investigation only progressed when the team separated:

```text
Initiating failure
Propagation
Amplification
User-visible symptom
Recovery mechanism
```

## Lesson

A real symptom is not automatically the root cause.

---

## 2. The First Plausible Explanation May Be Wrong

Garbage collection was initially the strongest hypothesis.

This was reasonable because the logs showed prolonged JVM pauses around incident windows.

The team applied valid runtime improvements:

- Runtime upgrade
- Garbage-collector change
- Garbage-collector tuning
- Heap adjustment

The incident still occurred.

## Lesson

A remediation can be technically correct without resolving the actual incident.

The investigation must continue until the entire failure chain is explained.

---

## 3. Infrastructure Can Be Healthy at the Wrong Level

CPU and memory remained within normal limits.

The VM remained reachable.

General infrastructure dashboards appeared healthy.

However, the Cassandra write path was still experiencing severe transient degradation.

## Lesson

Healthy CPU and memory do not prove healthy infrastructure.

For stateful and latency-sensitive workloads, storage behavior must be treated as a first-class reliability signal.

---

## 4. Short Incidents Require Persistent Telemetry

The degraded Cassandra node recovered automatically.

By the time engineers executed diagnostic commands, the environment frequently appeared normal.

Commands such as:

```bash
nodetool status
nodetool tpstats
nodetool compactionstats
nodetool info
```

remained useful, but they were often executed after recovery.

## Lesson

When incidents last seconds, the investigation must rely on:

- Persisted metrics
- Timestamped logs
- Historical dashboards
- Event correlation
- Baseline deviation
- Automatic evidence capture

Manual diagnosis alone is not fast enough.

---

## 5. Time Alignment Is More Valuable Than Metric Volume

The environment already produced many metrics.

The decisive improvement did not come from collecting the largest possible number of signals.

It came from aligning the correct signals within the same time window.

```text
Storage write latency
Cassandra write failures
Commit-log delay
Hints activity
JVM pause
Node availability
Gateway threads
Autoscaling
Client impact
```

## Lesson

Observability maturity is not measured by dashboard count.

It is measured by the ability to explain system behavior across layers.

---

## 6. Application Errors Can Originate Below the Application

The client-facing symptom appeared in frontend services and gateway workloads.

The failure origin was far below those layers.

```text
Client timeout
        ↓
Gateway backpressure
        ↓
Cassandra delay
        ↓
Storage write latency
        ↓
Storage virtualization
```

## Lesson

Troubleshooting must follow dependencies downward until the evidence stops.

Application teams need enough infrastructure understanding to investigate below the runtime.

---

## 7. Network Symptoms May Be Processing Symptoms

Cassandra peers reported dropped messages and temporary node unavailability.

This initially resembled a network issue.

The evidence showed that the affected node became locally unresponsive before peer communication failed.

## Lesson

A timeout between two nodes does not prove a network fault.

The sender or receiver may be too slow to process the message within the expected interval.

---

## 8. Garbage Collection Requires Context

GC duration increased during incident windows.

However:

- CPU was not saturated.
- Memory was not exhausted.
- Workload did not consistently explain the pauses.
- Runtime tuning did not eliminate the incidents.
- Storage latency aligned with the same failures.

## Lesson

GC must be interpreted together with:

- Application thread behavior
- Allocation rate
- Heap state
- CPU availability
- Storage behavior
- Database operations
- External dependencies

A GC pause can be a cause, an effect or an unrelated concurrent event.

---

## 9. Cassandra Write Paths Need I/O Isolation

The initial design placed several write-intensive activities on the same disk:

- SSTable writes
- Memtable flushes
- Compactions
- Commit-log synchronization
- Hints activity

The dedicated commit-log disk reduced contention on a latency-sensitive path.

## Lesson

Workloads with different I/O patterns should not automatically share the same storage device.

The commit log deserves special attention because it participates directly in write acknowledgement and durability.

---

## 10. Baseline Performance Matters More Than Peak Performance

The original storage tier supported bursting.

Burst capacity can appear attractive, but it is temporary and workload-dependent.

The final design increased the guaranteed baseline of:

- IOPS
- Throughput
- Write-path isolation

## Lesson

Latency-sensitive systems should be designed around sustainable baseline performance.

Burst capacity should be treated as additional headroom, not as the normal reliability model.

---

## 11. Capacity Is Not the Same as Performance

The disk upgrade increased capacity, but capacity was not the main objective.

The important improvements were:

- Higher baseline IOPS
- Higher baseline throughput
- Lower dependence on bursting
- Better workload isolation
- More predictable latency

## Lesson

Storage sizing must evaluate:

```text
Capacity
IOPS
Throughput
Latency
Queue behavior
Caching
Redundancy
Burst characteristics
```

Selecting a disk only by size is insufficient.

---

## 12. Caching Is a Workload-Specific Decision

The original write path used host caching configured as `Read/Write`.

The remediation changed latency-sensitive paths to `None`.

The investigation did not prove caching was the independent root cause.

## Lesson

Caching should not be enabled or disabled by habit.

It must be evaluated according to:

- Application consistency requirements
- Write durability
- Storage semantics
- Latency sensitivity
- Vendor guidance
- Observed behavior

---

## 13. Resilience and Performance Must Be Evaluated Together

The original storage redundancy model emphasized zone-level resilience.

The final design selected a different model for latency-sensitive database paths after evaluating the broader architecture.

Cassandra already distributed replicas across availability zones and used quorum consistency.

## Lesson

A reliability decision must consider the entire system.

Storage-level redundancy cannot be evaluated in isolation from:

- Database replication
- Failure domains
- Quorum behavior
- Recovery procedures
- Business requirements
- Latency objectives

This does not make one redundancy model universally superior.

It makes the decision workload-specific.

---

## 14. Quorum Protects Consistency but Exposes Slow Replicas

Local quorum provided important consistency and availability properties.

However, a slow replica could delay request completion or cause timeouts.

## Lesson

Distributed-system availability depends not only on whether nodes are running.

It depends on whether enough nodes respond within the required latency budget.

```text
Available node
≠
Responsive node
```

---

## 15. Automatic Recovery Can Hide Repeated Failures

The platform recovered through:

- Cassandra node recovery
- Connection redirection
- Gateway thread handling
- Autoscaling
- Request retry and queue drainage

These mechanisms reduced prolonged outages.

They also made the incidents appear brief and self-healing.

## Lesson

Self-healing without root-cause follow-up can normalize recurring reliability defects.

Recovery metrics should be analyzed together with failure frequency and user impact.

---

## 16. Autoscaling Does Not Fix Dependency Latency

The gateway scaled when thread pressure increased.

This added processing capacity but did not improve the Cassandra storage path.

## Lesson

Autoscaling is effective when demand exceeds capacity.

It is less effective when requests are blocked on a degraded dependency.

Scaling can absorb symptoms while increasing cost and complexity.

---

## 17. Frontend Timeouts Define the Visible Failure Window

The backend degradation lasted seconds.

The client-visible impact lasted longer because requests accumulated and frontend timeout thresholds were exceeded.

## Lesson

Timeouts across the service chain must be designed intentionally.

They should consider:

- Dependency latency
- Retry behavior
- Queueing
- Thread usage
- User experience
- Recovery behavior
- Failure amplification

Increasing timeouts blindly would only hide the storage issue and retain threads longer.

---

## 18. Hints Can Protect Availability and Increase Pressure

Hints support eventual delivery when replicas cannot acknowledge writes.

During an already degraded storage event, hints can create additional local writes.

## Lesson

A resilience mechanism can become an amplifier under resource degradation.

Hints should be monitored alongside:

- Write timeouts
- Node availability
- Disk latency
- Commit-log behavior
- Hints volume
- Recovery duration

---

## 19. Vendor Escalation Requires Evidence, Not Suspicion

The cloud infrastructure initially appeared healthy through standard metrics.

The provider investigation required repeated and time-aligned evidence.

The internal team supplied:

- Storage latency windows
- Cassandra logs
- Gateway impact
- JVM evidence
- Multiple occurrences
- Results from previously applied changes

## Lesson

Effective escalation requires a defensible technical narrative:

```text
What happened
When it happened
Where it started
How it propagated
What was ruled out
What evidence supports escalation
```

This produces better vendor collaboration than sending isolated screenshots or generic error messages.

---

## 20. Provider RCA and Local Remediation Can Coexist

The provider identified a platform-level storage condition.

The global correction was not yet available when the team needed to reduce production risk.

The team therefore implemented local architectural improvements.

## Lesson

An external root cause does not remove internal responsibility for risk reduction.

SRE teams should ask:

- What can be controlled locally?
- What can reduce recurrence?
- What can improve detection?
- What can limit impact?
- How will the provider correction be validated later?

---

## 21. Automation Is Part of the Reliability Fix

The remediation involved multiple nodes, disks, logical volumes, mount points and configuration changes.

Manual execution would create risk of inconsistency.

The process was automated using configuration management.

## Lesson

A production improvement is incomplete when it cannot be reproduced safely.

Automation should provide:

- Idempotence
- Preconditions
- Controlled execution
- Validation
- Failure stops
- Repeatability
- Auditability

---

## 22. Rolling Changes Must Preserve Quorum

The Cassandra architecture depended on a required number of responsive replicas.

The storage change therefore needed to proceed one node at a time.

## Lesson

Maintenance procedures for distributed systems must understand consistency and failure-domain rules.

A technically correct node-level procedure can still create an outage when executed concurrently across too many replicas.

---

## 23. Validation Must Use the Original Failure Signals

A change should not be declared successful only because:

- The service started.
- The node rejoined.
- The deployment completed.
- The change ticket closed.

The team used the same signals from the incident to validate recovery.

## Lesson

The strongest validation asks:

> Did the exact failure pattern stop recurring?

For this case, validation included:

- Storage write latency
- Cassandra write failures
- Commit-log behavior
- Node availability
- Gateway threads
- Autoscaling
- Client activity

---

## 24. Absence of Recurrence Is Evidence, Not Absolute Proof

No similar incident occurred during the first month after remediation.

This is strong positive evidence.

It does not prove permanent elimination.

## Lesson

Post-change statements should preserve uncertainty.

A credible conclusion is:

> The previous failure pattern did not recur during the initial observation period.

A less credible conclusion would be:

> The issue can never happen again.

---

## 25. Confidentiality Is Part of Engineering Quality

The original investigation included:

- Internal hostnames
- IP addresses
- Support cases
- Vendor communications
- Exact topology
- Production logs
- Business-impact data
- Personal and organizational information

None of that was required to communicate the engineering lesson publicly.

## Lesson

A strong public case study preserves technical depth while removing operational identity.

Anonymization should protect:

- Organizations
- Individuals
- Infrastructure
- Customers
- Credentials
- Proprietary communications
- Security-relevant details

---

## What Went Well

- The team continued investigating after initial JVM changes.
- Cross-layer dashboards were created.
- Incident signals were aligned in time.
- Multiple occurrences were compared.
- Storage was identified as the initiating failure mode.
- Evidence supported vendor escalation.
- Commit-log and data I/O were separated.
- Baseline storage performance increased.
- Changes were automated.
- Validation used end-to-end observability.
- No recurrence was observed during the initial monitoring period.

---

## What Could Be Improved

- Storage-specific SLIs could have existed earlier.
- Commit-log latency could have been monitored directly from the start.
- Composite alerts could have reduced investigation time.
- Burst-credit signals could have been retained proactively.
- Hints activity could have had stronger alerting.
- Cross-layer dashboards could have been standardized before the incident.
- Provider escalation criteria could have been documented earlier.
- Post-incident SLO and error-budget review remained pending.

---

## Recommended Preventive Controls

## Storage

- Monitor write and read latency.
- Monitor baseline and burst behavior.
- Track IOPS and throughput saturation.
- Review host-caching configuration.
- Separate incompatible I/O workloads.
- Reassess disk tier as workloads grow.

## Cassandra

- Monitor write and read failures.
- Monitor commit-log synchronization duration.
- Track dropped messages.
- Track hints activity.
- Monitor node responsiveness.
- Review compaction and flush behavior.

## Gateway

- Monitor worker-thread pressure.
- Monitor dependency latency.
- Track connection redirection.
- Review autoscaling frequency.
- Correlate backend delays with user impact.

## Incident Management

- Preserve short-event telemetry automatically.
- Use standardized evidence windows.
- Maintain hypothesis and evidence matrices.
- Define vendor-escalation requirements.
- Validate changes against original failure signals.

---

## Personal SRE Lesson

The deepest professional lesson from this incident was:

> To understand production reliability, an engineer must go below the visible application symptom and learn how the application behaves on the infrastructure where it runs.

That means understanding:

- Application threads
- Database internals
- JVM behavior
- Operating-system behavior
- Storage architecture
- Cloud abstractions
- Distributed-system consistency
- Recovery mechanisms

The investigation was successful because it did not stop at the first technology boundary.

---

## Final Engineering Principles

```text
Measure before changing.

Correlate before concluding.

Separate symptoms from causes.

Design for baseline performance.

Automate repeatable operations.

Validate through the full service path.

Preserve uncertainty where evidence is incomplete.

Protect confidential information when sharing knowledge.
```

---

## Related Documents

- [Case Overview](README.md)
- [Architecture](architecture.md)
- [Timeline](timeline.md)
- [Investigation](investigation.md)
- [Observability](observability.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Remediation](remediation.md)

---

## SRE Thinking

The most valuable result of an incident is not only restoring service.

It is improving the system and the engineering organization so that the next investigation becomes:

- Faster
- Safer
- More measurable
- More repeatable
- More defensible

A mature SRE practice turns a difficult incident into architecture, automation, observability and shared knowledge.