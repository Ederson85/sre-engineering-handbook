# Lab 05 - Disk I/O Bottleneck Investigation

**Module:** Linux  
**Category:** Lab  
**Level:** Intermediate  
**Estimated Time:** 30 minutes

---

# Objective

Investigate a production-like performance degradation caused by high Disk I/O.

The objective is to determine whether storage latency is responsible for application slowness before applying any mitigation.

---

# Scenario

Users report that an internal application has become significantly slower.

Monitoring shows:

- CPU utilization below 40%
- Memory utilization within normal limits
- Increased application response time
- Elevated storage latency

A scheduled backup job started approximately 20 minutes before the alerts.

You have SSH access to the affected server.

Your mission is to identify the bottleneck and determine the safest corrective action.

---

# Prerequisites

- Linux VM or Lab Environment
- Terminal access
- Basic Linux administration knowledge

> ⚠️ Do not stop production workloads without following your organization's operational procedures.

---

# Tasks

## Task 1 — Confirm the Server

Execute:

```bash
hostname
whoami
uptime
```

Questions:

- Am I connected to the correct server?
- Is the system responsive?

---

## Task 2 — Verify CPU Utilization

Execute:

```bash
top
```

Question:

Is CPU saturation causing the performance issue?

---

## Task 3 — Check Memory Activity

Execute:

```bash
free -h

vmstat 1 5
```

Observe:

- Available memory
- Swap activity
- I/O wait (`wa`)

Question:

Is memory pressure contributing to storage activity?

---

## Task 4 — Investigate Disk I/O

Execute:

```bash
iostat -xz 1 5
```

Observe:

- `%util`
- `await`
- `r/s`
- `w/s`
- `rkB/s`
- `wkB/s`

Questions:

- Is the storage device saturated?
- Is latency increasing?
- Are reads or writes dominant?

---

## Task 5 — Identify I/O Intensive Processes

Execute:

```bash
iotop
```

If unavailable:

```bash
pidstat -d 1 5
```

Question:

Which process is generating the highest I/O activity?

---

## Task 6 — Review Historical Disk Activity

Execute:

```bash
sar -d 1 5
```

Question:

Has storage utilization increased recently?

---

## Task 7 — Review Kernel Messages

Execute:

```bash
dmesg
```

Look for:

- I/O errors
- Filesystem warnings
- Storage controller messages

---

## Task 8 — Correlate Recent Changes

Confirm:

- Backup execution
- Large imports
- Database maintenance
- Recent deployments
- Storage maintenance

---

# Expected Result

At the end of this lab you should be able to answer:

- Is Disk I/O the bottleneck?
- Which process is generating storage activity?
- Is CPU contributing to the issue?
- Is memory contributing to the issue?
- What is the safest mitigation?
- Should the incident be escalated?

---

# Lessons Learned

Disk I/O bottlenecks are frequently misidentified as CPU or application issues.

A structured investigation helps isolate the true bottleneck before applying mitigation.

---

# 💡 SRE Thinking

Good SREs investigate systems holistically.

Applications, CPU, memory and storage are interconnected.

Always correlate multiple metrics before concluding where the bottleneck exists.

Evidence first.

Mitigation second.

Continuous improvement always.