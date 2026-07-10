# Memory Pressure Troubleshooting

**Module:** Linux  
**Category:** Troubleshooting

---

# Scenario

An alert indicates high memory utilization on a production Linux server.

Users report increased response times, and some applications may have become unstable.

The objective is to identify the root cause before applying any mitigation.

---

# Investigation Workflow

```
Alert

↓

Confirm Memory Pressure

↓

Identify Memory Consumers

↓

Check Swap Usage

↓

Analyze Kernel Messages

↓

Determine Root Cause

↓

Mitigate

↓

Validate Recovery
```

---

# Step 1 — Confirm Memory Pressure

```bash
free -h
```

Observe:

- Total memory
- Used memory
- Available memory
- Swap usage

Memory Pressure is better evaluated using **Available** memory rather than simply **Used** memory.

---

# Step 2 — Identify Top Memory Consumers

```bash
ps aux --sort=-%mem | head
```

Look for:

- Unexpected processes
- Rapid memory growth
- Duplicate processes
- Java applications
- Containers

---

# Step 3 — Monitor Memory in Real Time

```bash
top
```

or

```bash
htop
```

Observe:

- RES memory
- VIRT memory
- Swap activity
- CPU correlation

---

# Step 4 — Review Kernel Memory Information

```bash
cat /proc/meminfo
```

Important fields:

- MemAvailable
- Cached
- Buffers
- SwapFree
- SwapTotal

---

# Step 5 — Check for OOM Killer Events

```bash
dmesg | grep -i oom
```

or

```bash
journalctl -k | grep -i oom
```

If OOM Killer has terminated a process, identify:

- Which process was killed
- Timestamp
- Possible trigger

---

# Step 6 — Evaluate Swap Activity

```bash
vmstat 1 5
```

Pay attention to:

- si (swap in)
- so (swap out)

Continuous swap activity usually indicates memory pressure.

---

# Step 7 — Correlate with Recent Changes

Verify:

- Recent deployments
- Configuration changes
- Traffic spikes
- Batch jobs
- Backup execution

---

# Validation

After mitigation, confirm:

```bash
free -h

vmstat 1 5

top
```

Expected outcome:

- Available memory increases
- Swap stabilizes
- No new OOM events
- Applications respond normally

---

# Escalation

Escalate if:

- OOM events continue
- Memory keeps growing
- Root cause cannot be identified
- Business impact remains high

---

# 💡 SRE Thinking

Do not assume that adding more memory is the solution.

A disciplined SRE first determines whether the issue is caused by:

- Memory leak
- Application behavior
- Configuration
- Workload increase
- Infrastructure limitations

Mitigation without understanding the root cause often results in recurring incidents.