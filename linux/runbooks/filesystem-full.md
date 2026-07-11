# Filesystem Full Runbook

**Module:** Linux  
**Category:** Runbook  
**Severity:** Filesystem Full

---

# Alert

A filesystem has reached or is approaching 100% utilization.

Monitoring may also report:

- Disk utilization above threshold
- Log write failures
- Application errors
- Database write failures
- Deployment failures

---

# Possible Impact

- Applications cannot write data
- Log files stop growing
- Database operations fail
- New deployments fail
- Service degradation
- Operating system instability

---

# Prerequisites

Before applying any mitigation:

- Confirm the correct server and environment.
- Identify the affected filesystem.
- Verify business impact.
- Determine whether the service has redundancy.
- Capture evidence before deleting files.
- Follow change and incident management procedures.

---

# Diagnosis

## 1. Confirm the Server

```bash
hostname
uptime
```

---

## 2. Identify the Affected Filesystem

```bash
df -hT
```

Verify:

- Mounted filesystem
- Utilization
- Available space
- Filesystem type

---

## 3. Check Inode Utilization

```bash
df -i
```

A filesystem with free disk space may still fail if inode usage reaches 100%.

---

## 4. Locate Disk Usage

```bash
du -xhd1 /
```

Continue investigating the largest directories until the source is identified.

---

## 5. Find Large Files

```bash
find /var -type f -size +500M
```

Typical findings:

- Log files
- Backup files
- Core dumps
- Temporary files

---

## 6. Check Deleted but Open Files

```bash
lsof +L1
```

Deleted files held open by running processes continue consuming disk space.

---

## 7. Review Logs

```bash
journalctl -n 100 --no-pager
```

Look for:

- Filesystem errors
- Log rotation failures
- Write failures
- Application exceptions

---

# Mitigation

Always choose the safest mitigation.

Possible actions:

- Rotate oversized log files.
- Remove obsolete temporary files.
- Remove unnecessary backup artifacts.
- Restart the application only if deleted files remain open and restarting is approved.
- Expand filesystem capacity when required.

Never delete files without understanding why they exist.

---

# Validation

Confirm recovery:

```bash
df -hT

df -i

du -xhd1 /
```

Validate:

- Filesystem utilization decreased.
- Applications resumed normal operation.
- Logs are being written successfully.
- Monitoring alerts cleared.

---

# Rollback

If mitigation causes additional impact:

- Restore deleted files from backup when possible.
- Roll back recent deployments if related.
- Escalate to the storage or platform team.

---

# Escalation

Escalate when:

- Disk usage continues increasing.
- Storage expansion is required.
- Filesystem corruption is suspected.
- Root cause cannot be determined.

---

# Post Incident

Document:

- Timeline
- Root cause
- Mitigation
- Validation
- Lessons learned

Update this runbook whenever a new incident improves the investigation process.

---

# 💡 SRE Thinking

A full filesystem is usually the result of another problem.

Deleting files may restore service temporarily, but understanding why disk usage increased is what prevents the incident from happening again.

Preserve evidence.

Restore service safely.

Eliminate the root cause.