# Real World - High CPU After Deployment

**Module:** Linux  
**Category:** Real World  
**Severity:** High

---

# Incident Summary

Shortly after a production deployment, monitoring reported sustained CPU utilization above 95%.

Users began reporting increased response times and intermittent request failures.

---

# Environment

- Production
- Linux
- Java Application
- systemd Service
- Monitoring Platform

---

# Symptoms

- CPU above 95%
- High Load Average
- Slow application response
- Increased latency
- Health check failures

---

# Investigation

The investigation followed the standard High CPU workflow.

## Confirm the server

```bash
hostname
uptime
```

---

## Identify CPU consumers

```bash
top
```

```bash
ps aux --sort=-%cpu | head
```

The Java application process was consuming almost all available CPU.

---

## Validate the process

```bash
ps -fp <PID>
```

The process matched the recently deployed application.

---

## Review application logs

```bash
journalctl -u application.service -n 100 --no-pager
```

The logs showed repeated exceptions immediately after deployment.

---

## Validate recent changes

The deployment timeline matched the beginning of the CPU increase.

---

# Root Cause

A software defect introduced during deployment caused an infinite processing loop.

The application continuously retried failed operations, consuming excessive CPU resources.

---

# Resolution

The deployment was rolled back.

The application service was restarted.

CPU utilization returned to normal.

---

# Validation

The following commands confirmed recovery:

```bash
top
uptime
systemctl status application.service
```

Monitoring confirmed:

- CPU utilization normalized
- Load Average decreased
- Response time returned to baseline
- No new errors observed

---

# Lessons Learned

High CPU was not the root cause.

The deployment introduced a software defect that manifested as high CPU utilization.

Rollback procedures and deployment validation significantly reduced recovery time.

---

# 💡 SRE Thinking

Always correlate infrastructure metrics with recent changes.

Many infrastructure alerts originate from application behavior.

High CPU is often the consequence—not the cause—of the incident.