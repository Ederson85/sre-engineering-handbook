# Filesystem Commands

**Module:** Linux  
**Category:** Reference  
**Level:** Beginner

---

# Overview

Disk usage problems are among the most common causes of production incidents.

Checking filesystem usage should always be part of a server health check.

---

# df

## Purpose

Displays filesystem utilization.

```bash
df -h
```

---

# du

## Purpose

Displays directory size.

```bash
du -sh *
```

---

# lsblk

## Purpose

Displays block devices.

```bash
lsblk
```

---

# What to Check

- Filesystems above 80%
- Unexpected disk growth
- Mounted disks
- Available capacity

---

# Next Step

Proceed to the Linux Health Check Lab.