# Disk I/O Bottleneck Runbook

**Module:** Linux  
**Category:** Runbook  
**Severity:** High Storage Latency

---

# Alert

Monitoring reports increased storage latency or sustained high Disk I/O utilization.

Related alerts may include:

- High application response time
- Database latency
- Elevated I/O wait
- Slow file operations
- Backup execution delays

---

# Possible Impact

- Slow application response
- Database degradation
- Increased API latency
- Timeout errors
- Batch job delays
- Service instability

---

# Prerequisites

Before applying mitigation:

- Confirm the affected server and environment.
- Verify business impact.
- Identify critical applications using the storage.
- Capture evidence before restarting services.
- Follow incident and change management procedures.

---

# Diagnosis

## 1. Confirm the Server

```bash
hostname
uptime
```

---

## 2. Verify CPU and Load

```bash
top
```

Confirm whether CPU saturation is contributing to the issue.

---

## 3. Check Memory Activity

```bash
free -h

vmstat 1 5
```

Observe:

- Available memory
- Swap activity
- I/O wait (`wa`)

---

## 4. Investigate Disk I/O

```bash
iostat -xz 1 5
```

Pay attention to:

- %util
- await
- r/s
- w/s
- rkB/s
- wkB/s

---

## 5. Identify I/O Intensive Processes

```bash
iotop
```

If unavailable:

```bash
pidstat -d 1 5
```

Determine which processes generate the highest read/write activity.

---

## 6. Review Historical Disk Activity

```bash
sar -d 1 5
```

Look for:

- Throughput changes
- Device utilization
- Latency spikes

---

## 7. Review Kernel Messages

```bash
dmesg
```

Look for:

- I/O errors
- Disk failures
- Filesystem warnings
- Storage controller messages

---

## 8. Validate Recent Changes

Confirm whether:

- Backup jobs started.
- Large imports are running.
- Database maintenance is active.
- Storage changes occurred.
- Recent deployments introduced new workloads.

---

# Mitigation

Always choose the least disruptive mitigation.

Possible actions include:

- Pause non-critical backup jobs.
- Reschedule heavy batch processing.
- Optimize storage-intensive applications.
- Move workloads to less busy storage.
- Scale storage resources when necessary.

Avoid restarting services before understanding the root cause.

---

# Validation

Confirm recovery:

```bash
iostat -xz 1 5

vmstat 1 5
```

Validate:

- Lower `await`
- Reduced `%util`
- Lower I/O wait
- Improved application response time
- Monitoring alerts cleared

---

# Rollback

If mitigation increases impact:

- Resume suspended jobs if appropriate.
- Restore previous storage configuration.
- Escalate to the infrastructure or storage team.

---

# Escalation

Escalate when:

- Storage latency persists.
- Hardware degradation is suspected.
- SAN/NAS infrastructure is affected.
- Root cause cannot be identified.

---

# Post Incident

Document:

- Timeline
- Root cause
- Mitigation
- Validation
- Lessons learned

Update this runbook whenever new operational knowledge is acquired.

---

# 💡 SRE Thinking

High Disk I/O is often a symptom rather than the root cause.

Investigate workload patterns, storage behavior and recent operational changes before applying corrective actions.

Measure.

Correlate.

Mitigate.

Validate.