# 02 - Filesystem

## Why Filesystems Matter for SRE

Filesystem issues are a common cause of production incidents. A full disk can stop logs, databases, queues, package managers, application writes and even system services.

For an SRE, the goal is not only to see that a disk is full. The goal is to understand which filesystem is affected, what is growing, whether the growth is expected and what can be cleaned safely.

---

## What to Check

- Mounted filesystems and utilization.
- Filesystem type and mount point.
- Large directories inside the affected mount point.
- Log growth under `/var/log`.
- Temporary files under `/tmp` and application-specific temp directories.
- Inodes, especially when many small files are created.

---

## Useful Commands

```bash
df -hT
df -ih
lsblk
mount | column -t
du -xhd1 / 2>/dev/null | sort -h
```

---

## SRE Interpretation

High disk usage is a symptom. Before deleting anything, identify the owner and purpose of the files.

In production, prefer evidence collection first:

- Which mount point is full?
- Is it root, `/var`, `/home`, `/opt`, application data or a dedicated volume?
- Is the growth caused by logs, dumps, temporary files or business data?
- Is the affected service redundant?
- Is there a retention policy?

---

## Key Takeaway

Disk cleanup is a mitigation, not a root cause analysis. Safe SRE practice is to identify the growth pattern, recover capacity carefully and create prevention through monitoring, retention or automation.
