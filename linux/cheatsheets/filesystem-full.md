# Filesystem Full Cheatsheet

> Quick reference for investigating Filesystem Full incidents on Linux systems.

---

# Check Filesystem Usage

```bash
df -hT
```

Displays:

- Filesystem type
- Mounted filesystem
- Total size
- Used space
- Available space
- Utilization percentage

---

# Check Inode Usage

```bash
df -i
```

Useful when disk space is available but new files cannot be created.

---

# Find Largest Directories

```bash
du -xhd1 /
```

Continue investigating:

```bash
du -xhd1 /var
```

---

# Find Large Files

```bash
find /var -type f -size +500M
```

Typical targets:

- Log files
- Core dumps
- Backup files
- Temporary files

---

# Find Deleted but Open Files

```bash
lsof +L1
```

These files still consume disk space until the owning process releases them.

---

# List Block Devices

```bash
lsblk
```

---

# View Mounted Filesystems

```bash
mount
```

---

# Review System Logs

```bash
journalctl -n 100 --no-pager
```

---

# Validation

```bash
df -hT

df -i

du -xhd1 /
```

Expected:

- Free space increased
- Inode usage normalized
- Applications resumed normal operation
- Monitoring alerts cleared

---

# Related Commands

- df
- du
- find
- lsof
- lsblk
- mount
- journalctl

---

# 💡 SRE Thinking

A full filesystem is not always caused by large files.

Always investigate:

- Inodes
- Deleted but open files
- Log growth
- Backup retention
- Application behavior

Never delete data before understanding why it exists.