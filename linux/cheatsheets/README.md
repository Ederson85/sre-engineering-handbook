# Linux SRE Cheatsheet

Quick command reference for Linux server health checks and incident investigation.

---

## Server Identification

```bash
hostname
whoami
uname -a
```

---

## System Health

```bash
uptime
top
vmstat 1 5
```

---

## Memory

```bash
free -m
ps aux --sort=-%mem | head
```

---

## CPU

```bash
top
ps aux --sort=-%cpu | head
```

---

## Filesystem

```bash
df -hT
du -xhd1 . 2>/dev/null | sort -h
lsblk
```

---

## Network

```bash
ip addr
ip route
ss -tuln
ping <host>
curl http://<host>
```

---

## Logs

```bash
journalctl -p warning -n 100 --no-pager
dmesg -T | tail -n 100
tail -f /var/log/syslog
```

---

## Quick Investigation Flow

```text
hostname
↓
uptime
↓
free -m
↓
df -hT
↓
top
↓
ps aux
↓
journalctl
```
