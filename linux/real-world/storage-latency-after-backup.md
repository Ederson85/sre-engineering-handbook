# Real World - Storage Latency After Backup

**Module:** Linux  
**Category:** Real World  
**Severity:** High

---

# Incident Summary

During business hours, users reported that several internal applications became significantly slower.

Monitoring showed:

- High application latency
- CPU utilization below 40%
- Normal memory utilization
- Elevated storage latency

No application errors were reported.

---

# Environment

- Production
- Linux
- Virtual Machine
- Shared Storage
- Database Server
- Enterprise Backup Solution

---

# Symptoms

- Slow application response
- Increased API latency
- Database queries taking longer than usual
- High I/O wait
- Increased storage utilization
- No CPU or memory saturation

---

# Investigation

The investigation followed the standard Disk I/O workflow.

---

## Confirm the server

```bash
hostname
uptime
```

---

## Verify CPU utilization

```bash
top
```

CPU remained below expected utilization thresholds.

The issue was not CPU saturation.

---

## Check memory

```bash
free -h

vmstat 1 5
```

Memory remained stable.

However, I/O wait (`wa`) increased significantly.

---

## Investigate storage

```bash
iostat -xz 1 5
```

The storage device presented:

- High `%util`
- Increased `await`
- Elevated write throughput

Storage latency was confirmed.

---

## Identify I/O intensive processes

```bash
iotop
```

A backup process was responsible for most write operations.

---

## Review kernel messages

```bash
dmesg
```

No storage hardware errors were detected.

---

## Validate recent operational changes

The operations calendar confirmed that a full backup had started approximately twenty minutes before the first monitoring alert.

The backup was executing during peak business hours.

---

# Root Cause

The backup job generated sustained write activity on shared storage.

The storage subsystem became saturated, increasing latency for all applications using the same disks.

No application defect or infrastructure failure was identified.

The incident was caused by an operational scheduling decision.

---

# Resolution

The backup was paused after confirming business impact.

The job was rescheduled to execute during the maintenance window.

Storage latency returned to normal within a few minutes.

Application response times recovered without restarting any services.

---

# Validation

Recovery was confirmed using:

```bash
iostat -xz 1 5

vmstat 1 5

top
```

Monitoring confirmed:

- Reduced storage latency
- Lower `%util`
- Lower `await`
- Reduced I/O wait
- Normal application response time

---

# Lessons Learned

Infrastructure was healthy.

Applications were healthy.

The storage subsystem behaved correctly.

The operational schedule created resource contention during peak usage.

Proper workload scheduling is an important reliability practice.

---

# 💡 SRE Thinking

Not every production incident is caused by software bugs or infrastructure failures.

Sometimes the root cause is an operational decision.

Understanding workload behavior is just as important as understanding Linux commands.

Reliable systems require good engineering and good operational practices.