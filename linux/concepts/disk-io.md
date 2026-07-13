# Disk I/O Bottleneck

**Module:** Linux  
**Category:** Concept

---

# Overview

Disk I/O (Input/Output) represents read and write operations performed between the operating system and storage devices.

When storage cannot process requests fast enough, applications experience increased latency even if CPU and memory utilization remain low.

Disk I/O bottlenecks are common in production environments and often impact databases, APIs and file-intensive workloads.

Understanding storage behavior is essential for Site Reliability Engineers.

---

# Why it Matters

High Disk I/O latency may lead to:

- Slow application response times
- Database performance degradation
- Increased API latency
- Timeout errors
- Long deployment times
- Service instability

Unlike CPU or memory issues, Disk I/O problems often appear as system slowness without high resource utilization.

---

# Common Causes

- Backup jobs
- Log ingestion
- Large file transfers
- Database checkpoints
- Storage contention
- Insufficient IOPS
- Slow disks
- Virtualization storage contention
- Container image extraction

---

# Key Concepts

## IOPS

IOPS (Input/Output Operations Per Second) measures how many read and write operations a storage device can perform each second.

Higher IOPS generally indicate better storage performance.

---

## Throughput

Throughput represents the amount of data transferred over time.

Usually measured in:

- MB/s
- GB/s

---

## Latency

Latency measures how long storage takes to complete an I/O request.

Lower latency generally means better application performance.

---

## Queue Depth

Queue Depth represents the number of pending I/O operations waiting for storage resources.

Large queues often indicate storage contention.

---

## Disk Utilization

High utilization may indicate that the storage device is operating near its maximum capacity.

However, utilization alone should never be used to determine storage health.

Always correlate utilization with latency.

---

# Common Investigation Commands

```bash
iostat -xz 1

vmstat 1

iotop

pidstat -d 1

sar -d 1

dmesg
```

---

# What to Observe

- Disk utilization
- Read latency
- Write latency
- Queue depth
- Read/write throughput
- Processes generating I/O
- Storage-related kernel messages

---

# Related Commands

- iostat
- vmstat
- iotop
- pidstat
- sar
- dmesg

---

# Typical Investigation Flow

Alert

↓

High application latency

↓

CPU normal

↓

Memory normal

↓

Investigate Disk I/O

↓

Identify bottleneck

↓

Determine root cause

↓

Mitigate safely

↓

Validate recovery

---

# Related Topics

- Server Health Check
- High CPU Investigation
- Memory Pressure Investigation
- Filesystem Full Investigation

---

# 💡 SRE Thinking

Applications rarely report "Disk I/O Bottleneck."

They report symptoms such as slow responses, timeouts or failed requests.

An experienced SRE learns to correlate application behavior with storage metrics before taking corrective actions.

Measure first.

Understand second.

Act last.