# Real World - Disk Full After Log Growth

**Module:** Linux  
**Category:** Real World  
**Severity:** High

---

# Incident Summary

A production monitoring platform reported that the `/var` filesystem had reached **100% utilization**.

Shortly after the alert:

- Applications failed to write logs.
- New deployments could not complete.
- Users reported intermittent errors.

The incident affected multiple services running on the same Linux server.

---

# Environment

- Production
- Linux
- Java Application
- systemd Services
- Centralized Monitoring
- Log Rotation Enabled

---

# Symptoms

- `/var` filesystem at 100%
- Log write failures
- Application errors
- Deployment failures
- Increased response time
- Monitoring alerts

---

# Investigation

The investigation followed the standard Filesystem Full workflow.

---

## Confirm the server

```bash
hostname
uptime
```

---

## Identify the affected filesystem

```bash
df -hT
```

The `/var` filesystem showed **100% utilization**.

---

## Verify inode utilization

```bash
df -i
```

Inode usage remained within normal limits.

The problem was storage capacity, not inode exhaustion.

---

## Locate disk usage

```bash
du -xhd1 /var
```

The `/var/log` directory accounted for most of the consumed space.

---

## Find large files

```bash
find /var/log -type f -size +500M
```

Several application log files had grown beyond expected limits.

---

## Check deleted but open files

```bash
lsof +L1
```

No deleted files remained open.

---

## Review logs

```bash
journalctl -n 100 --no-pager
```

The investigation revealed repeated log rotation failures after a recent configuration change.

---

## Validate recent changes

A deployment performed the previous day had introduced an incorrect log rotation configuration.

Application logs continued growing without being rotated.

---

# Root Cause

A misconfigured log rotation policy prevented old log files from being archived and removed.

Continuous log growth exhausted the available disk space in the `/var` filesystem.

---

# Resolution

The log rotation configuration was corrected.

Oversized log files were archived according to operational procedures.

After validation, obsolete archived logs were removed.

Disk utilization immediately returned to normal.

---

# Validation

The following commands confirmed recovery:

```bash
df -hT

du -xhd1 /var

journalctl -n 50 --no-pager
```

Monitoring confirmed:

- Filesystem utilization below threshold
- Applications writing logs normally
- Successful deployment execution
- No additional storage alerts

---

# Lessons Learned

Filesystem Full was only the visible symptom.

The real issue was an operational configuration error that disabled proper log rotation.

Regular validation of log retention policies can prevent similar incidents.

---

# 💡 SRE Thinking

Deleting files would have restored space temporarily.

Understanding why the files continued growing prevented the incident from recurring.

Good SREs solve the operational problem, not only the immediate symptom.