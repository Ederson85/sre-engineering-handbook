# Lab 04 - Filesystem Full Investigation

**Module:** Linux  
**Category:** Lab  
**Level:** Intermediate  
**Estimated Time:** 25 minutes

---

# Objective

Investigate a Filesystem Full alert using a structured SRE investigation workflow.

The objective is to identify the root cause of disk utilization before deleting files or applying any mitigation.

---

# Scenario

A monitoring platform reports that the `/var` filesystem has reached **98% utilization**.

Users report:

- Application errors
- Log write failures
- Slow response times

A deployment scheduled for the environment has also failed due to insufficient disk space.

You have SSH access to the affected server.

Your mission is to investigate the incident and determine the safest corrective action.

---

# Prerequisites

- Linux VM or Lab Environment
- Terminal access
- Basic Linux knowledge

> ⚠️ Never delete files in a production environment before understanding why they exist.

---

# Tasks

## Task 1 — Confirm the Server

Execute:

```bash
hostname
whoami
uptime
```

Questions:

- Am I connected to the correct server?
- Is the system responsive?

---

## Task 2 — Identify the Affected Filesystem

Execute:

```bash
df -hT
```

Observe:

- Mounted filesystem
- Utilization
- Available space

Question:

Which filesystem is full?

---

## Task 3 — Check Inode Usage

Execute:

```bash
df -i
```

Question:

Is the problem disk space or inode exhaustion?

---

## Task 4 — Locate Disk Usage

Execute:

```bash
du -xhd1 /
```

Continue investigating the largest directory:

```bash
du -xhd1 /var
```

Question:

Which directory consumes the most disk space?

---

## Task 5 — Find Large Files

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

## Task 6 — Check Deleted but Open Files

Execute:

```bash
lsof +L1
```

Question:

Are deleted files still consuming disk space?

---

## Task 7 — Review Logs

Execute:

```bash
journalctl -n 100 --no-pager
```

Look for:

- Log rotation failures
- Filesystem errors
- Application write failures

---

## Task 8 — Correlate with Recent Changes

Confirm:

- Recent deployments
- Backup jobs
- Log rotation configuration
- Increased application traffic

---

# Expected Result

At the end of this lab you should be able to answer:

- Which filesystem is full?
- What is consuming disk space?
- Are inodes exhausted?
- Are deleted files still open?
- Is mitigation required?
- What is the safest corrective action?

---

# Lessons Learned

Deleting files without understanding the root cause often leads to recurring incidents.

Always investigate:

- Disk utilization
- Inode usage
- Large files
- Deleted but open files
- Recent operational changes

---

# 💡 SRE Thinking

A full filesystem is an operational symptom.

The real problem is understanding **why** storage consumption increased.

Evidence first.

Safe mitigation second.

Continuous improvement always.