# Filesystem Full Troubleshooting

**Module:** Linux  
**Category:** Troubleshooting

---

# Scenario

A monitoring platform reports that a filesystem has reached 100% utilization.

Applications are failing to write data, log files are no longer growing and users begin reporting service degradation.

The objective is to identify the root cause before deleting files or restarting services.

---

# Investigation Workflow

```
Alert

↓

Identify the affected filesystem

↓

Verify inode utilization

↓

Locate disk usage

↓

Find large files

↓

Check deleted but open files

↓

Determine root cause

↓

Mitigate safely

↓

Validate recovery
```

---

# Step 1 — Identify the Affected Filesystem

Execute:

```bash
df -hT
```

Observe:

- Mounted filesystem
- Filesystem type
- Capacity
- Available space
- Utilization percentage

---

# Step 2 — Check Inode Usage

Execute:

```bash
df -i
```

A filesystem may report free disk space but still be unable to create new files if inode usage reaches 100%.

---

# Step 3 — Locate Disk Usage

Execute:

```bash
du -xhd1 /
```

Continue investigating the largest directory:

```bash
du -xhd1 /var
```

Repeat until the primary source of disk usage is identified.

---

# Step 4 — Find Large Files

Execute:

```bash
find /var -type f -size +500M
```

Look for:

- Log files
- Backup files
- Core dumps
- Temporary files

---

# Step 5 — Check Deleted but Open Files

Execute:

```bash
lsof +L1
```

If deleted files are still held open by running processes, disk space will not be released until the process closes the file.

---

# Step 6 — Review Logs

Execute:

```bash
journalctl -n 100 --no-pager
```

Look for:

- Disk write failures
- Log rotation errors
- Filesystem errors
- Application exceptions

---

# Step 7 — Correlate with Recent Changes

Verify:

- Recent deployments
- Backup execution
- Log rotation failures
- Increased application traffic
- New services

---

# Validation

After mitigation:

```bash
df -hT

df -i

du -xhd1 /
```

Confirm:

- Filesystem utilization decreased
- Available space increased
- Applications resumed normal operation
- Logs are being written successfully

---

# Escalation

Escalate when:

- Root cause cannot be identified.
- Filesystem usage continues increasing.
- Storage expansion is required.
- Multiple services are affected.

---

# 💡 SRE Thinking

A full filesystem is rarely the root cause.

Deleting files without understanding why they were created may restore service temporarily, but the incident will likely return.

Investigate first.

Mitigate safely.

Prevent recurrence.