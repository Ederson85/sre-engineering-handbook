# Memory Pressure Runbook

**Module:** Linux  
**Category:** Runbook  
**Severity:** High Memory Utilization

---

# Alert

Memory utilization remains above the defined threshold for more than 5 minutes.

Monitoring may also report:

- Low `MemAvailable`
- Sustained swap-in or swap-out activity
- Memory PSI pressure
- OOM or allocation failure events
- Application degradation correlated with memory pressure

---

# Possible Impact

- Slow application response
- Increased latency
- Swap activity
- Application instability
- Process termination by OOM Killer
- Service degradation

---

# Prerequisites

Before applying mitigation:

- Confirm the correct host and environment.
- Confirm the affected service and business impact.
- Check whether the service has redundancy.
- Identify the process owner.
- Verify whether a deployment or change is in progress.
- Follow the incident and change management process.
- Capture evidence before restarting or scaling the service.

---

# Diagnosis

## 1. Confirm the Server

```bash
hostname
uptime
```

---

## 2. Check Memory Utilization

```bash
free -h
```

Verify:

- Available memory
- Used memory
- Swap usage

---

## 3. Identify Memory Consumers

```bash
ps aux --sort=-%mem | head
```

If necessary:

```bash
top
```

or

```bash
htop
```

---

## 4. Inspect the Process

```bash
ps -fp <PID>
```

Determine whether the process is expected and if memory consumption is abnormal.

---

## 5. Review Logs

```bash
journalctl -u <service-name> -n 100 --no-pager
```

Check for:

- Exceptions
- Memory allocation failures
- Restart loops
- Unexpected application behavior

---

## 6. Check for OOM Killer

```bash
dmesg | grep -i oom
```

or

```bash
journalctl -k | grep -i oom
```

If an OOM event occurred:

- Identify the terminated process.
- Record the timestamp.
- Correlate with monitoring data.

---

## 7. Validate Recent Changes

Confirm whether:

- A deployment occurred.
- Configuration changed.
- Traffic increased.
- A scheduled job is running.

---

# Mitigation

Always prefer the safest action.

Possible mitigations include:

- Restart the affected application (if appropriate).
- Roll back a recent deployment.
- Scale the application horizontally.
- Increase memory allocation only after identifying the root cause.

Avoid clearing Linux cache as a troubleshooting shortcut.

---

# Validation

Confirm recovery using:

```bash
free -h

vmstat 1 5 5

top
```

Validate that:

- Available memory increased.
- Swap usage stabilized.
- No new OOM events occurred.
- Application performance returned to normal.

---

# Rollback

If mitigation increases impact:

- Restore the previous application version.
- Revert recent configuration changes.
- Escalate immediately if service health continues to degrade.

---

# Escalation

Escalate when:

- Memory consumption continues to increase.
- OOM Killer events persist.
- Root cause cannot be determined.
- Multiple services are affected.

---

# Post Incident

Document:

- Timeline
- Root cause
- Mitigation
- Validation
- Lessons learned

Update the runbook whenever a new lesson improves the investigation process.

---

# 💡 SRE Thinking

Memory Pressure is rarely solved by adding more RAM.

Reliable systems are built by understanding why memory consumption increased.

Evidence first.

Mitigation second.

Continuous improvement always.