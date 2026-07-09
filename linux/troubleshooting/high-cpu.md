# High CPU Troubleshooting

**Module:** Linux  
**Category:** Troubleshooting  
**Level:** Intermediate

---

## Problem

A monitoring platform reports sustained CPU utilization above the defined threshold.

Users may experience:

- Increased response time
- Timeouts
- Slow applications
- Failed health checks

---

## Investigation Steps

### Step 1 — Confirm the server

```bash
hostname
whoami
uptime
```

Verify that you are connected to the correct host.

---

### Step 2 — Check Load Average

```bash
uptime
```

Review:

- 1-minute load
- 5-minute load
- 15-minute load

Compare the Load Average with the number of CPU cores:

```bash
nproc
```

Example:

- 4 CPU cores
- Load Average = 3.2 → acceptable
- Load Average = 12.5 → overloaded

---

### Step 3 — Identify CPU consumers

```bash
top
```

or

```bash
ps aux --sort=-%cpu | head
```

Questions:

- Which process is consuming CPU?
- Is it expected?
- Is it persistent?

---

### Step 4 — Inspect the process

```bash
ps -fp <PID>
```

If needed:

```bash
lsof -p <PID>
```

Understand what the process is doing before taking action.

---

### Step 5 — Review logs

If managed by systemd:

```bash
journalctl -u <service-name> -n 100 --no-pager
```

Look for:

- Exceptions
- Restart loops
- Errors
- Deployment failures

---

### Step 6 — Validate recent changes

Ask:

- Was there a deployment?
- Was configuration changed?
- Did traffic increase?
- Is there a scheduled job running?

---

## Decision

If the process is healthy but overloaded:

→ investigate application behavior.

If the process is stuck or unhealthy:

→ continue with the High CPU Runbook.

---

## Related Documents

- High CPU Concept
- High CPU Runbook
- Linux Commands Reference