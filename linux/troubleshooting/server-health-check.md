# Server Health Check Troubleshooting

**Module:** Linux  
**Category:** Troubleshooting  
**Level:** Beginner

---

## Problem

A Linux server is reported as slow or unresponsive.

Before restarting services or escalating the incident, perform a structured health check.

---

## Investigation Steps

## Step 1 — Confirm the Server

```bash
hostname
whoami
pwd
```

Verify that you are connected to the correct server.

---

## Step 2 — Check System Load

```bash
uptime
```

Review:

- System uptime
- Load Average

---

## Step 3 — Check CPU Usage

```bash
top
ps aux --sort=-%cpu | head
```

Look for:

- High CPU utilization
- Runaway processes

---

## Step 4 — Check Memory

```bash
free -m
vmstat 1 5
ps aux --sort=-%mem | head
```

Look for:

- Low available memory
- Swap usage
- High memory consumers

---

## Step 5 — Check Filesystem

```bash
df -hT
du -xhd1 / 2>/dev/null | sort -h
```

Look for:

- Filesystems above 80%
- Unexpected disk usage

---

## Step 6 — Check Network

```bash
ip addr
ip route
ss -tuln
```

Verify:

- Network interfaces
- Routes
- Listening services

---

## Step 7 — Check Logs

```bash
journalctl -p warning -n 100 --no-pager
dmesg -T | tail -n 100
```

Look for:

- Errors
- Service failures
- Hardware issues

---

## Decision

If the operating system is healthy, continue investigating the application, dependency, database or network path.

If infrastructure problems are found, resolve them before troubleshooting the application.

---

## Related Documents

- [Server Health Check Concept](../concepts/server-health.md)
- [Linux Reference](../reference/README.md)
- [Lab 01 - Server Health Check](../labs/lab-01-server-health-check.md)
- [Server Health Check Runbook](../runbooks/server-health-check.md)
- [Linux SRE Cheatsheet](../cheatsheets/README.md)
