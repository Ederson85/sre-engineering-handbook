# High CPU Cheatsheet

> Quick reference for investigating High CPU utilization on Linux systems.

---

# Check CPU Usage

```bash
top
```

```bash
htop
```

```bash
uptime
```

---

# Find CPU Consumers

```bash
ps aux --sort=-%cpu | head
```

---

# View Process Details

```bash
ps -fp <PID>
```

---

# Per-Core CPU Usage

```bash
mpstat -P ALL 1
```

> Requires the `sysstat` package.

---

# Process Statistics

```bash
pidstat -u 1
```

---

# Thread Analysis

```bash
top -H -p <PID>
```

---

# Check System Load

```bash
uptime
```

---

# Check Service Status

```bash
systemctl status <service>
```

```bash
systemctl --failed
```

---

# Check Logs

```bash
journalctl -u <service> -n 100 --no-pager
```

---

# Graceful Process Termination

```bash
kill -15 <PID>
```

---

# Force Process Termination

```bash
kill -9 <PID>
```

> ⚠️ Use only if the process does not respond to SIGTERM.

---

# Validation

```bash
top
```

```bash
uptime
```

```bash
systemctl status <service>
```

---

# Related Commands

- top
- htop
- ps
- pidstat
- mpstat
- uptime
- systemctl
- journalctl
- kill

---

# 💡 SRE Thinking

High CPU is usually **a symptom**, not the root cause.

Before restarting a service or terminating a process:

- Confirm the alert.
- Identify the process consuming CPU.
- Check application logs.
- Verify recent deployments or configuration changes.
- Collect evidence before taking action.

Think like an SRE:

> **Investigate first. Mitigate second. Learn always.**