# Real World - Memory Leak After Release

**Module:** Linux  
**Category:** Real World  
**Severity:** Critical

---

# Incident Summary

Approximately 30 minutes after a production deployment, monitoring detected a continuous increase in memory consumption.

Initially, the application remained responsive. Over time, memory availability decreased, swap usage increased and response times became unstable.

Eventually, the Linux kernel invoked the Out-Of-Memory (OOM) Killer.

---

# Environment

- Production
- Linux
- Java Application
- systemd Service
- Monitoring Platform

---

# Symptoms

- Memory utilization above 95%
- Available memory continuously decreasing
- Swap activity increasing
- Application latency
- OOM Killer events
- Automatic process restart

---

# Investigation

The investigation followed the standard Memory Pressure workflow.

---

## Confirm the server

```bash
hostname
uptime
```

---

## Check memory usage

```bash
free -h
```

Memory usage remained consistently high while available memory continued to decrease.

---

## Identify memory consumers

```bash
ps aux --sort=-%mem | head
```

The Java application was consuming significantly more memory than expected.

---

## Review kernel messages

```bash
dmesg | grep -i oom
```

The kernel log confirmed that the application process had been terminated by the OOM Killer.

---

## Review application logs

```bash
journalctl -u application.service -n 100 --no-pager
```

Repeated allocation failures were identified shortly after the deployment.

---

## Validate recent changes

Deployment history showed that a new version had been released approximately 30 minutes before the alert.

---

# Root Cause

The new application version introduced a memory leak.

Objects allocated during request processing were never released, causing continuous memory growth until system resources were exhausted.

---

# Resolution

The deployment was rolled back to the previous stable version.

After rollback:

- Memory utilization stabilized.
- Swap activity stopped.
- No additional OOM events occurred.
- Application response times returned to normal.

---

# Validation

The following commands confirmed service recovery:

```bash
free -h

vmstat 1

top

journalctl -u application.service -n 50 --no-pager
```

Monitoring confirmed:

- Stable memory utilization
- Healthy application
- No new kernel OOM events

---

# Lessons Learned

Memory Pressure was only the visible symptom.

The actual problem was a software defect introduced during deployment.

Monitoring trends, kernel logs and deployment history were essential to identify the true root cause.

---

# 💡 SRE Thinking

Memory leaks rarely appear immediately after a deployment.

Investigate memory trends over time rather than relying on a single snapshot.

Correlate infrastructure metrics with deployment history and application behavior.

Reliable incident response is based on evidence, not assumptions.