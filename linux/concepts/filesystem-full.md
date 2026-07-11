# Filesystem Full

**Module:** Linux  
**Category:** Concept

---

# Overview

A Filesystem Full condition occurs when a filesystem reaches its storage capacity and can no longer accept new data.

This is one of the most common production incidents in Linux environments and can affect applications, databases, logging systems and operating system stability.

Understanding how Linux stores data and how filesystems behave under high utilization is essential for Site Reliability Engineers.

---

# Why it Matters

A full filesystem can lead to:

- Application failures
- Inability to write logs
- Database errors
- Deployment failures
- Service interruptions
- System instability

Even a single full partition, such as `/var`, may impact critical services while the rest of the system appears healthy.

---

# Common Causes

- Log files growing without rotation
- Core dump accumulation
- Temporary files
- Backup files
- Large application artifacts
- Docker image accumulation
- Kubernetes container logs
- User-generated files
- Misconfigured retention policies

---

# Key Concepts

## Filesystem

A filesystem organizes how data is stored and retrieved from storage devices.

---

## Disk Usage

Disk usage refers to the percentage of allocated storage already consumed.

High utilization should always be investigated before reaching 100%.

---

## Inodes

A filesystem may become unusable even with available disk space if all inodes are consumed.

Always verify both storage utilization and inode usage.

---

## Mount Points

Linux separates storage into mount points.

Each mount point must be investigated independently.

---

## Deleted but Open Files

A deleted file may continue consuming disk space if a running process still holds it open.

This is a common source of confusion during production incidents.

---

# Investigation Commands

```bash
df -hT

df -i

du -xhd1 /

find /var -type f -size +500M

lsof +L1

lsblk

mount
```

---

# What to Observe

- Filesystem utilization
- Available space
- Inode utilization
- Largest directories
- Large files
- Deleted but open files
- Mounted filesystems

---

# Typical Investigation Flow

Alert

↓

Identify affected filesystem

↓

Locate disk usage

↓

Identify large files

↓

Check deleted open files

↓

Determine root cause

↓

Mitigate safely

↓

Validate recovery

---

# Related Topics

- Server Health Check
- Linux Filesystem
- Linux Logs
- Troubleshooting Methodology

---

# 💡 SRE Thinking

Deleting files immediately may restore service, but it can also destroy valuable evidence.

Experienced SREs identify the root cause before removing data whenever possible.

Preserve evidence.

Restore service safely.

Prevent recurrence.