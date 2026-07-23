# Architecture

This document describes the anonymized architecture involved in the incident and the storage design changes implemented during remediation.

---

## Architecture Overview

The platform consisted of:

- A cloud-hosted API gateway
- Containerized gateway workloads
- Automatic horizontal scaling
- Distributed Cassandra clusters
- Availability-zone distribution
- Quorum-based consistency
- Cloud-managed block storage
- Centralized observability

The API gateway depended on Cassandra for operational data required during request processing.

---

## Logical Application Flow

```text
Client Request
      ↓
Frontend Services
      ↓
API Gateway Workloads
      ↓
Cassandra Cluster
      ↓
Quorum Confirmation
      ↓
Request Processing Continues
```

Cassandra stored information such as:

- API metadata
- Runtime policies
- Quota-related data
- Operational tables and keyspaces

---

## Gateway Layer

The gateway layer ran multiple containerized workloads.

Important characteristics included:

- Multiple gateway instances
- Automatic connection redirection
- Thread-based autoscaling
- Minimum and maximum scaling boundaries
- Dependency on Cassandra responsiveness
- Short frontend timeout thresholds

When Cassandra became temporarily slow, gateway workloads accumulated waiting threads.

The autoscaling mechanism detected thread pressure and increased the number of gateway instances.

This behavior helped absorb load but did not eliminate the underlying database latency.

---

## Cassandra Topology

Each Cassandra cluster contained multiple nodes distributed across availability zones.

```text
Availability Zone A
└── Cassandra Node A

Availability Zone B
└── Cassandra Node B

Availability Zone C
└── Cassandra Node C
```

The design provided fault tolerance across zones.

Critical operations used a local quorum consistency model.

```text
Write Request
      ↓
Coordinator Node
      ↓
Replication to Peer Nodes
      ↓
Quorum Acknowledgement
      ↓
Operation Confirmed
```

For a request to succeed, the required number of Cassandra replicas needed to respond within the configured timeout.

A temporary delay in one node could therefore affect quorum completion and increase request latency.

---

## Connection Behavior During Degradation

Gateway workloads maintained connectivity with the Cassandra cluster.

When one Cassandra node became temporarily unavailable:

```text
Gateway Connection
        ↓
Slow Cassandra Node
        ↓
Timeout or Failed Operation
        ↓
Driver Redirects to Healthy Node
        ↓
Workload Continues
```

The gateway workloads were not recreated during this process.

Connections were redirected automatically by the Cassandra integration layer.

However, the short interruption caused:

- Thread accumulation
- Request backpressure
- Temporary autoscaling
- Client-facing timeouts
- Short-lived reduction in successful activity

---

## Initial Storage Architecture

Each Cassandra virtual machine used separate managed disks for the operating system, data and operational work.

```text
Cassandra VM

├── OS Disk
│   └── Operating system
│
├── Data Disk
│   ├── Cassandra data
│   ├── SSTables
│   ├── Commit log
│   └── Hints activity
│
└── Work Disk
    ├── Upgrade files
    ├── Temporary backups
    └── Operational artifacts
```

The data disk was responsible for multiple write-intensive workloads.

This created contention between:

- SSTable writes
- Memtable flushes
- Compactions
- Commit-log synchronization
- Hints creation

The initial disk design used:

- A mid-tier premium disk
- Zone-redundant storage
- Credit-based bursting characteristics
- Host caching configured as `Read/Write`

The configuration favored resilience, but the workload was highly sensitive to write-latency variation.

---

## Logical Volume Design

The mounted Cassandra filesystems were implemented using logical volumes.

```text
Managed Disk
      ↓
Logical Volume
      ↓
Mounted Filesystem
      ↓
Cassandra Data Path
```

The logical volume abstraction allowed the operating system to expose only the required filesystem size while retaining the underlying managed-disk capacity.

This detail is generalized because the exact internal allocation is not relevant to the engineering conclusions.

---

## Incident Propagation Path

The architecture allowed a short storage event to propagate across several layers.

```text
Cloud Storage Latency
        ↓
Data Volume Write Delay
        ↓
Commit-Log Synchronization Delay
        ↓
Cassandra WriteTimeoutException
        ↓
Hints and Mutation Pressure
        ↓
Temporary Node Degradation
        ↓
Quorum Completion Delay
        ↓
Gateway Thread Accumulation
        ↓
Autoscaling Activity
        ↓
Frontend Timeouts
```

The duration at each layer was different:

- Storage and Cassandra impact: seconds
- Gateway recovery: longer than the original storage event
- Client-facing effect: visible for approximately one or two minutes

---

## Why the Problem Was Difficult to Detect

The architecture was resilient enough to recover automatically.

That resilience also made the incident harder to investigate.

The system:

- Redirected connections
- Recovered nodes automatically
- Scaled gateway workloads
- Restored traffic without manual intervention
- Returned to normal before most commands could capture the event

As a result, static snapshots taken after the incident often appeared healthy.

The investigation required time-aligned observability across every layer.

---

## Remediated Storage Architecture

The final design separated latency-sensitive Cassandra workloads.

```text
Cassandra VM

├── OS Disk
│   └── Operating system
│
├── Data Disk
│   ├── SSTables
│   ├── Memtable flushes
│   └── Compactions
│
├── Commit Disk
│   └── Cassandra commit log
│
└── Work Disk
    ├── Upgrade files
    ├── Temporary backups
    └── Operational artifacts
```

The main architectural changes included:

- Higher-performance data disk
- Dedicated commit-log disk
- Higher baseline IOPS
- Higher baseline throughput
- Reduced dependency on bursting
- Locally redundant storage for latency-sensitive paths
- Host caching configured as `None`
- Isolation between data and commit-log writes

---

## Before and After

### Before

```text
Data Disk
├── SSTables
├── Compactions
├── Memtable Flushes
├── Commit Log
└── Hints
```

Characteristics:

- Shared write path
- Mid-tier performance
- Variable write demand
- Credit-based bursting dependency
- Host caching enabled
- Higher contention risk

### After

```text
Data Disk
├── SSTables
├── Compactions
├── Memtable Flushes
└── Hints

Commit Disk
└── Commit Log
```

Characteristics:

- Isolated commit-log path
- Higher baseline performance
- More predictable latency
- Reduced write contention
- Host caching disabled
- Improved workload separation

---

## Storage Trade-Off

The original redundancy model prioritized zone-level resilience.

The remediated design prioritized predictable latency for a highly latency-sensitive database workload.

This was not a universal statement that one redundancy model is better than another.

It was an engineering trade-off based on:

- Workload sensitivity
- Failure behavior
- Observed latency variation
- Quorum requirements
- Recovery capabilities
- Existing availability-zone architecture

---

## Architecture Principles Reinforced

This incident reinforced several design principles:

- Separate workloads with different I/O patterns.
- Avoid sharing commit-log and data paths for latency-sensitive systems.
- Evaluate baseline performance, not only burst capacity.
- Treat storage caching as an application-specific decision.
- Design for both resilience and latency predictability.
- Observe infrastructure and application behavior together.
- Understand how quorum consistency amplifies node-level latency.

---

## Related Documents

- [Case Overview](README.md)
- [Timeline](timeline.md)
- [Investigation](investigation.md)
- [Observability](observability.md)
- [Root Cause Analysis](root-cause-analysis.md)
- [Remediation](remediation.md)
- [Lessons Learned](lessons-learned.md)

---

## SRE Thinking

A resilient architecture can hide a failing component long enough for the incident to become intermittent.

Automatic recovery is valuable, but it does not remove the need to understand the failure path.

Good SRE architecture makes both failure recovery and failure visibility possible.