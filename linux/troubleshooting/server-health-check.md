# Server Health Check Troubleshooting

**Module:** Linux  
**Category:** Troubleshooting  
**Level:** Beginner

---

# Problem

A Linux server is reported as slow or unresponsive.

Before restarting services or escalating the incident, perform a structured health check.

---

# Investigation Steps

## Step 1 — Confirm the Server

```bash
hostname
whoami
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
df -h
du -sh /*
```

Look for:

- Filesystems above 80%
- Unexpected disk usage

---

## Step 6 — Check Network

```bash
ip addr
ip route
ss -tulnp
```

Verify:

- Network interfaces
- Routes
- Listening services

---

## Step 7 — Check Logs

```bash
journalctl -xe
dmesg
```

Look for:

- Errors
- Service failures
- Hardware issues

---

# Decision

If the operating system is healthy, continue investigating the application.

If infrastructure problems are found, resolve them before troubleshooting the application.

---

# Related Documents

- Server Health Check Concept
- Linux Reference
- Lab 01 - Server Health Check
- Linux Cheatsheet