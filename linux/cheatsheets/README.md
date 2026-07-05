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
df -h
du -sh *
lsblk
```

---

## Network

```bash
ip addr
ip route
ss -tulnp
ping <host>
curl http://<host>
```

---

## Logs

```bash
journalctl -xe
dmesg
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
df -h
↓
top
↓
ps aux
↓
journalctl
```