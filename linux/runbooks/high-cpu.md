# High CPU Runbook

**Module:** Linux  
**Category:** Runbook  
**Severity:** High CPU Utilization

---

## Alert

CPU utilization remains above the defined threshold for more than 5 minutes.

---

## Possible Impact

- Increased latency
- Slow application response
- Timeouts
- Failed health checks
- Service degradation

---

# Diagnosis

## 1. Confirm server

```bash
hostname
uptime
```

---

## 2. Identify CPU consumers

```bash
top
```

or

```bash
ps aux --sort=-%cpu | head
```

---

## 3. Validate process

```bash
ps -fp <PID>
```

---

## 4. Inspect logs

```bash
journalctl -u <service> -n 100 --no-pager
```

---

## 5. Check recent deployment

Confirm whether:

- a deployment occurred
- configuration changed
- traffic increased

---

# Mitigation

Always prefer graceful actions.

If managed by systemd:

```bash
systemctl restart <service>
```

If necessary:

```bash
kill -15 <PID>
```

Only if absolutely necessary:

```bash
kill -9 <PID>
```

---

# Validation

After mitigation verify:

```bash
uptime
top
free -m
systemctl status <service>
```

Confirm:

- CPU returned to normal
- Application is healthy
- Monitoring recovered

---

# Rollback

If mitigation increases impact:

- restart previous version
- restore previous configuration
- escalate immediately

---

# Escalation

Escalate when:

- root cause is unknown
- CPU remains high
- multiple services affected
- customer impact continues

---

# Post Incident

- Document timeline
- Identify root cause
- Improve monitoring
- Update runbook if necessary

---

# 💡 SRE Thinking

High CPU is rarely the problem.

It is usually the symptom.

Investigate the workload before terminating processes.

Evidence first.
Mitigation second.