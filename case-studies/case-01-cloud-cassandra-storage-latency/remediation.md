# Remediation

This document describes the engineering decisions and architectural changes implemented to reduce exposure to transient storage latency.

The remediation was designed before the cloud-provider platform correction was fully available.

The team therefore focused on changes that could be controlled, automated, validated and rolled back within the application environment.

---

## Remediation Objectives

The remediation needed to achieve the following outcomes:

1. Reduce contention between Cassandra write workloads.
2. Increase baseline storage performance.
3. Improve write-latency predictability.
4. Reduce dependency on burst behavior.
5. Isolate the commit log from data-file operations.
6. Remove host caching from latency-sensitive storage paths.
7. Preserve operating-system and work-disk isolation.
8. Automate the implementation to reduce operational risk.
9. Validate recovery through the same observability signals used during the investigation.

---

## Remediation Strategy

The team selected a layered remediation strategy.

```text
Storage Performance
        +
Workload Isolation
        +
Caching Review
        +
Redundancy Trade-Off
        +
Configuration Automation
        +
Post-Change Observability
```

No single change was treated as a guaranteed independent fix.

The remediation package was designed to reduce multiple contributing factors at the same time.

---

## Initial Architecture

Before remediation, the Cassandra virtual machines used separate disks for the operating system, Cassandra data and operational work.

However, the Cassandra data disk handled several write-intensive activities.

```text
OS Disk
└── Operating system

Data Disk
├── Cassandra data
├── SSTables
├── Memtable flushes
├── Compactions
├── Commit log
└── Hints

Work Disk
├── Upgrade artifacts
├── Temporary backups
└── Operational files
```

The initial storage characteristics included:

- Mid-tier premium managed storage
- Lower baseline IOPS than the final design
- Lower baseline throughput than the final design
- Credit-based bursting characteristics
- Zone-redundant storage
- Host caching configured as `Read/Write`
- Shared data and commit-log I/O

---

## Identified Design Risks

The initial architecture exposed Cassandra to several risks.

## Shared Write Contention

The data disk received writes from:

- Commit-log synchronization
- Memtable flushes
- SSTable creation
- Compactions
- Hints activity

These operations have different patterns but competed for the same storage path.

---

## Variable Performance

The original disk tier provided a lower baseline and supported burst behavior.

Burst capacity can be useful, but a latency-sensitive database should not depend on temporary performance for normal reliability.

---

## Host Caching on the Write Path

The critical Cassandra write path used host caching configured as `Read/Write`.

The investigation did not prove caching was the initiating cause.

However, it introduced another behavior layer in a path where predictable write acknowledgement was important.

---

## Resilience and Latency Trade-Off

The original storage redundancy model prioritized zone-level resilience.

The incident demonstrated that resilience and latency predictability needed to be assessed together.

A durable storage design is not sufficient when short latency spikes can violate database and frontend timeouts.

---

## Decision Criteria

The final design was evaluated using the following criteria:

- Baseline IOPS
- Baseline throughput
- Write-latency predictability
- Separation of I/O workloads
- Cassandra commit-log requirements
- Quorum sensitivity
- Availability-zone architecture
- Operational recoverability
- Cost
- Automation feasibility
- Rollback capability
- Observability after deployment

The goal was not simply to select the largest disk.

The goal was to create a more predictable storage architecture for the workload.

---

## Change 1 — Data Disk Upgrade

The Cassandra data disk was upgraded from a mid-tier premium disk to a higher-performance premium tier.

The final data disk used the default higher-tier baseline of approximately:

```text
5,000 IOPS
200 MB/s throughput
```

Exact internal capacity allocations were intentionally generalized.

## Expected Benefits

- Higher baseline IOPS
- Higher baseline throughput
- Reduced dependence on bursting
- More consistent SSTable writes
- More predictable compaction behavior
- Greater tolerance for short write-intensive periods

## Important Distinction

The improvement came primarily from baseline performance and predictability.

The capacity increase was not the main engineering objective.

---

## Change 2 — Dedicated Commit-Log Disk

A dedicated premium disk was added for the Cassandra commit log.

## Before

```text
Data Disk
├── SSTables
├── Memtable flushes
├── Compactions
├── Hints
└── Commit log
```

## After

```text
Data Disk
├── SSTables
├── Memtable flushes
├── Compactions
└── Hints

Commit Disk
└── Commit log
```

## Why This Was Important

The commit log is part of Cassandra's critical write path.

Separating it from data-file activity reduced competition with:

- Memtable flushes
- SSTable writes
- Compactions
- Hints

This improved workload isolation and reduced the chance that background data activity would delay commit-log synchronization.

---

## Change 3 — Host Caching

Host caching was changed from:

```text
Read/Write
```

to:

```text
None
```

for the latency-sensitive Cassandra data and commit-log paths.

## Rationale

The objective was to:

- Remove an additional caching layer from critical writes
- Reduce behavioral variability
- Align the storage path with database write requirements
- Make latency measurements more representative of the managed storage path

## Evidence Boundary

The investigation did not prove that host caching independently caused the incident.

The change was part of a broader effort to simplify and stabilize the write path.

---

## Change 4 — Redundancy Model

The team changed the redundancy model for latency-sensitive Cassandra disks after evaluating:

- Existing availability-zone distribution
- Cassandra replication
- Local quorum behavior
- Application-level recovery
- Storage durability
- Latency predictability
- Failure-domain trade-offs

The final design selected locally redundant storage for the critical data and commit-log paths.

## Important Qualification

This decision does not imply:

```text
LRS is always better than ZRS
```

It means:

> For this specific replicated, multi-zone and latency-sensitive workload, the team selected the redundancy model that best matched the required balance between resilience and write-latency predictability.

---

## Final Storage Architecture

```text
Cassandra Virtual Machine

├── OS Disk
│   └── Operating system
│
├── Data Disk
│   ├── Cassandra data
│   ├── SSTables
│   ├── Memtable flushes
│   ├── Compactions
│   └── Hints
│
├── Commit Disk
│   └── Cassandra commit log
│
└── Work Disk
    ├── Upgrade artifacts
    ├── Temporary backups
    └── Operational files
```

The operating-system disk remained separate from the Cassandra data path.

The mounted filesystems were exposed through logical volumes.

---

## Before and After Comparison

| Area | Before | After |
|---|---|---|
| Data storage tier | Mid-tier premium | Higher-tier premium |
| Baseline IOPS | Lower | Approximately 5,000 |
| Baseline throughput | Lower | Approximately 200 MB/s |
| Commit log | Shared with data | Dedicated disk |
| Data and commit contention | Present | Reduced |
| Burst dependency | Higher | Reduced |
| Host caching | `Read/Write` | `None` |
| Redundancy model | Zone-redundant | Locally redundant for critical paths |
| Storage layout | Three disks | Four disks |
| Deployment method | Existing configuration | Automated controlled change |

---

## Configuration Changes

The Cassandra configuration was updated so that the commit log used the dedicated mount point.

A generalized representation is:

```yaml
data_file_directories:
  - /data/cassandra

commitlog_directory: /commitlog/cassandra
```

These paths are illustrative.

They do not represent actual production directories.

---

## Logical Volume Changes

The managed disks were attached to the virtual machines and exposed through logical volumes.

A generalized implementation flow was:

```text
Attach managed disk
        ↓
Detect block device
        ↓
Create or extend physical-volume configuration
        ↓
Create volume group or use approved volume group
        ↓
Create logical volume
        ↓
Create filesystem
        ↓
Create mount point
        ↓
Persist mount configuration
        ↓
Apply ownership and permissions
        ↓
Update Cassandra path
```

The exact storage commands and internal naming were intentionally excluded.

---

## Automation with Ansible

The remediation process was automated using configuration management.

Automation reduced the risk of inconsistent changes across Cassandra nodes.

## Automation Responsibilities

The automation handled or validated:

- Managed-disk visibility
- Block-device identification
- Logical-volume creation
- Filesystem creation
- Mount-point creation
- Persistent mount configuration
- Ownership and permissions
- Cassandra directory preparation
- Configuration-file updates
- Service state validation
- Post-change verification

---

## Automation Safety Principles

The automation was designed to be:

- Idempotent
- Node-aware
- Environment-aware
- Validated before mutation
- Executed in controlled batches
- Capable of stopping on failed preconditions
- Compatible with operational change procedures

---

## Example Automation Flow

```text
Pre-check node health
        ↓
Confirm correct environment and host
        ↓
Confirm quorum is healthy
        ↓
Validate attached storage
        ↓
Prepare logical volume and filesystem
        ↓
Mount dedicated commit-log path
        ↓
Stop or drain the selected node safely
        ↓
Move or initialize commit-log data according to procedure
        ↓
Update Cassandra configuration
        ↓
Start Cassandra
        ↓
Validate node recovery
        ↓
Observe before continuing to the next node
```

The actual production automation is confidential and is not included in this repository.

---

## Deployment Strategy

The changes were applied through controlled maintenance windows.

A rolling approach was required because Cassandra depended on quorum availability.

## Rolling Change Model

```text
Validate cluster health
        ↓
Select one node
        ↓
Remove or drain it according to procedure
        ↓
Apply storage and configuration changes
        ↓
Return node to service
        ↓
Validate cluster membership
        ↓
Validate replication and request behavior
        ↓
Observe stability
        ↓
Proceed to the next node
```

Only one failure domain was changed at a time.

---

## Preconditions

Before changing each node, the team validated:

- Correct host and environment
- Cluster health
- Required number of responsive replicas
- Absence of unrelated active incidents
- Change approval
- Backup and recovery readiness
- New disk attachment
- Logical-volume prerequisites
- Monitoring availability
- Rollback path

---

## Change Safety

The deployment followed these principles:

- Preserve quorum.
- Change one node at a time.
- Capture baseline metrics before the change.
- Avoid simultaneous changes across availability zones.
- Stop when validation fails.
- Do not proceed while the cluster is degraded.
- Keep the previous configuration available for rollback.
- Validate both technical and client-facing behavior.

---

## Validation Per Node

After changing a node, the team verified:

- Cassandra process running
- Node returning to the cluster
- Expected node status
- Correct data mount
- Correct commit-log mount
- Correct ownership and permissions
- No new filesystem errors
- No commit-log path errors
- No unexpected dropped messages
- Stable JVM behavior
- Normal storage latency
- Successful gateway connectivity

---

## Cluster-Level Validation

After completing the rolling deployment, the team validated:

- All Cassandra nodes responsive
- Local quorum available
- Stable replication
- Normal read and write behavior
- No recurring node-down events
- Gateway connections operating normally
- Thread levels returning to baseline
- Autoscaling remaining stable
- Client activity remaining stable

---

## Observability-Based Validation

The same dashboards used to diagnose the incident were used to verify remediation.

## Storage

Expected:

- Write latency within the normal range
- No spikes in the previously observed range
- Stable IOPS and throughput
- No abnormal queue behavior

## Cassandra

Expected:

- Stable write success
- Stable read success
- No unusual commit-log delays
- No recurring dropped-message pattern
- No temporary node unavailability

## JVM

Expected:

- No incident-correlated prolonged pauses
- Stable heap behavior
- No recurrence of the previous failure window

## Gateway

Expected:

- Stable worker-thread levels
- Reduced backend failures
- No incident-driven connection redirection
- No abnormal autoscaling events

## Client

Expected:

- Stable successful activity
- No short-lived timeout pattern
- Normal end-to-end recovery behavior

---

## Post-Change Results

During the initial observation period:

- Storage write latency remained in the normal range of tens of milliseconds.
- Previous spikes in the hundreds of milliseconds were not observed.
- Cassandra nodes remained responsive.
- Gateway errors decreased.
- Thread behavior stabilized.
- No similar incident recurred.

The environment was observed for approximately one month after the changes.

---

## Rollback Strategy

Rollback needed to preserve cluster availability.

A generalized rollback plan included:

1. Stop changes if any node failed validation.
2. Keep the node isolated until its state was understood.
3. Restore the previous Cassandra path configuration when safe.
4. Restore the previous mount configuration if required.
5. Reattach or remount the previous storage path.
6. Restart Cassandra using the approved recovery procedure.
7. Validate node health before rejoining normal traffic.
8. Escalate if quorum or data consistency was at risk.

Rollback was evaluated per node rather than as an immediate cluster-wide reversal.

---

## Residual Risks

The remediation reduced exposure but did not eliminate every possible risk.

Residual risks included:

- Cloud platform storage defects
- Future write-latency variation
- Compaction-related I/O pressure
- Hints growth after replica degradation
- Quorum sensitivity to slow nodes
- Configuration drift
- Capacity growth
- Changes in workload behavior
- Dependence on provider-level correction

---

## Follow-Up Actions

Recommended follow-up work included:

- Continue post-change monitoring
- Track the provider platform correction
- Review storage latency thresholds
- Add composite incident alerts
- Monitor commit-log synchronization duration
- Monitor dropped messages and hints
- Review disk capacity and performance periodically
- Maintain automation tests
- Document the rolling change procedure
- Review SLOs and error-budget impact
- Reassess the redundancy trade-off as platform capabilities evolve

---

## What the Remediation Did Not Claim

The remediation did not claim that:

- Every storage-latency event is caused by the same provider defect.
- Higher-tier disks eliminate every Cassandra performance issue.
- LRS is universally preferable to ZRS.
- Host caching is always inappropriate.
- Dedicated commit-log disks replace capacity planning.
- The absence of recurrence for one month proves permanent elimination.
- The provider-level issue no longer requires follow-up.

These boundaries preserve the technical credibility of the case.

---

## Remediation Outcome Statement

> The engineering team reduced exposure to transient storage latency by increasing baseline disk performance, separating Cassandra data and commit-log I/O, disabling host caching on latency-sensitive paths and automating a controlled rolling deployment. During the first month of post-change observation, the previous failure pattern did not recur.

---

## Related Documents

- [Case Overview](README.md)
- [Architecture](architecture.md)
- [Timeline](timeline.md)
- [Investigation](investigation.md)
- [Observability](observability.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Lessons Learned](lessons-learned.md)

---

## SRE Thinking

A remediation should address the failure mode, not only the visible symptom.

Restarting Cassandra could have restored the node.

Adding gateway instances could have absorbed more threads.

Increasing frontend timeouts could have hidden some failures.

None of those actions would have improved the storage write path.

The durable improvement came from changing the architecture beneath the symptom and validating the result through the complete service path.