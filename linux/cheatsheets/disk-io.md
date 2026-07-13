# Disk I/O Bottleneck Cheatsheet

> Quick reference for investigating Disk I/O performance issues on Linux systems.

---

# Check Overall Disk I/O

```bash
iostat -xz 1 5
```

Observe:

- %util
- await
- r/s
- w/s
- rkB/s
- wkB/s

---

# Check CPU and I/O Wait

```bash
vmstat 1 5
```

Pay attention to:

- wa (I/O wait)
- bi (blocks in)
- bo (blocks out)

---

# Identify I/O Intensive Processes

```bash
iotop
```

If unavailable:

```bash
pidstat -d 1 5
```

---

# Historical Disk Activity

```bash
sar -d 1 5
```

Useful for identifying:

- Throughput changes
- Latency spikes
- Device utilization

---

# Check Kernel Messages

```bash
dmesg
```

Look for:

- I/O errors
- Filesystem warnings
- Disk failures
- Storage controller issues

---

# Validate System Load

```bash
uptime

top
```

---

# Validation

```bash
iostat -xz 1 5

vmstat 1 5
```

Expected:

- Lower `await`
- Reduced `%util`
- Lower `wa`
- Stable application response times

---

# Related Commands

- iostat
- vmstat
- iotop
- pidstat
- sar
- dmesg

---

# 💡 SRE Thinking

High storage latency is rarely identified by a single metric.

Always correlate:

- Application latency
- CPU utilization
- Memory usage
- Disk latency
- I/O wait
- Running workloads

Avoid focusing on a single metric when investigating performance problems.