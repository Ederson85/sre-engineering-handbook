# Memory Pressure Cheatsheet

> Quick reference for investigating Memory Pressure on Linux systems.

---

# Check Memory Usage

```bash
free -h
```

---

# Real-Time Monitoring

```bash
top
```

```bash
htop
```

---

# Find Memory Consumers

```bash
ps aux --sort=-%mem | head
```

---

# View Process Details

```bash
ps -fp <PID>
```

---

# Kernel Memory Information

```bash
cat /proc/meminfo
```

Important fields:

- MemAvailable
- Cached
- Buffers
- SwapFree
- SwapTotal

---

# Monitor Memory Activity

```bash
vmstat 1 5
```

Pay attention to:

- si (swap in)
- so (swap out)

---

# Check OOM Killer Events

```bash
dmesg | grep -i oom
```

or

```bash
journalctl -k | grep -i oom
```

---

# Review Application Logs

```bash
journalctl -u <service-name> -n 100 --no-pager
```

---

# Validation

```bash
free -h

vmstat 1 5

top
```

Expected:

- Available memory increases
- Swap activity stabilizes
- No new OOM events
- Application performance returns to normal

---

# Related Commands

- free
- top
- htop
- ps
- vmstat
- journalctl
- dmesg
- cat

---

# 💡 SRE Thinking

High memory utilization does not always indicate Memory Pressure.

Focus on:

- Available memory
- Swap activity
- OOM events
- Application behavior

Investigate before increasing memory or restarting services.