# Disk I/O Bottleneck Troubleshooting

**Module:** Linux  
**Category:** Troubleshooting

---

# Scenario

Users report that applications are responding slowly.

Monitoring indicates increased response times, but CPU and memory utilization remain within normal levels.

The objective is to determine whether storage performance is the source of the degradation.

---

# Investigation Workflow

```
Alert

↓

High latency

↓

Check CPU

↓

Check Memory

↓

Investigate Disk I/O

↓

Identify storage bottleneck

↓

Determine root cause

↓

Mitigate safely

↓

Validate recovery
```

---

# Step 1 — Verify System Load

Execute:

```bash
uptime

top
```

Observe:

- Load Average
- CPU utilization
- Running processes

Question:

Is CPU saturation causing the latency?

---

# Step 2 — Check Memory

Execute:

```bash
free -h

vmstat 1
```

Observe:

- Available memory
- Swap activity
- IO wait (wa)

Question:

Is memory pressure causing excessive disk activity?

---

# Step 3 — Investigate Disk I/O

Execute:

```bash
iostat -xz 1
```

Observe:

- %util
- await
- r/s
- w/s
- rkB/s
- wkB/s

Questions:

- Is the disk saturated?
- Is latency increasing?
- Are read or write operations dominant?

---

# Step 4 — Identify I/O Intensive Processes

Execute:

```bash
iotop
```

If unavailable:

```bash
pidstat -d 1
```

Identify:

- Processes generating excessive reads
- Processes generating excessive writes

---

# Step 5 — Review Historical Activity

Execute:

```bash
sar -d 1
```

Observe:

- Read throughput
- Write throughput
- Device utilization

---

# Step 6 — Review Kernel Messages

Execute:

```bash
dmesg
```

Look for:

- Disk errors
- Controller failures
- Filesystem warnings
- I/O timeout messages

---

# Step 7 — Correlate Recent Changes

Verify:

- Backup execution
- Large data imports
- Database maintenance
- Batch jobs
- Storage maintenance
- Recent deployments

---

# Validation

After mitigation:

```bash
iostat -xz 1

vmstat 1
```

Confirm:

- Lower storage latency
- Reduced disk utilization
- Improved application response time
- Monitoring alerts cleared

---

# Escalation

Escalate when:

- Storage latency remains high.
- Hardware degradation is suspected.
- SAN or NAS infrastructure is affected.
- Root cause cannot be identified.

---

# 💡 SRE Thinking

High application latency does not always indicate a CPU problem.

Always investigate the complete resource chain before drawing conclusions.

Applications consume CPU.

CPU accesses memory.

Memory depends on storage.

Understanding this relationship helps identify the true bottleneck.