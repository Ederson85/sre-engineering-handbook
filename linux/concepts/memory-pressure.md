# Memory Pressure

**Module:** Linux  
**Category:** Concept

---

# Overview

Memory Pressure occurs when the operating system does not have enough available memory to satisfy application demands efficiently.

As memory utilization increases, the Linux kernel begins reclaiming memory, using swap (if available) and, in extreme situations, invoking the Out-Of-Memory (OOM) Killer to terminate processes.

Understanding Memory Pressure is essential for Site Reliability Engineers because it directly impacts application performance, latency and service availability.

---

# Why it matters

High memory utilization can lead to:

- Increased application latency
- Swap activity
- Performance degradation
- OOM Killer events
- Application crashes
- Node instability

Memory Pressure is often confused with high memory usage.

High memory utilization is not necessarily a problem if sufficient memory is still available and the system remains responsive.

---

# Common Causes

- Memory leaks
- Applications with excessive memory consumption
- Large caches
- Insufficient RAM
- Misconfigured JVM heap sizes
- Container memory limit violations
- Sudden traffic spikes

---

# Key Concepts

## Used Memory

Memory actively used by applications and the operating system.

---

## Available Memory

Memory immediately available for new processes without significant performance impact.

---

## Cache

Linux aggressively uses free memory as filesystem cache.

This improves performance and should not be considered a problem by itself.

---

## Buffers

Temporary memory used by the kernel for block device operations.

---

## Swap

Disk space used as virtual memory.

Occasional swap usage may be acceptable.

Heavy swap activity usually indicates memory pressure.

---

## OOM Killer

When the kernel cannot allocate additional memory, it selects one or more processes to terminate in order to recover the system.

OOM events should always be investigated.

---

# Investigation Commands

```bash
free -h

vmstat 1 5

top

htop

ps aux --sort=-%mem | head

cat /proc/meminfo

dmesg | grep -i oom

journalctl -k
```

---

# What to Observe

- Available Memory
- Swap usage
- Memory growth over time
- Top memory-consuming processes
- OOM Killer events
- Cache behavior
- System responsiveness

---

# Typical Investigation Flow

Alert

↓

Confirm Memory Pressure

↓

Identify top consumers

↓

Analyze logs

↓

Determine root cause

↓

Apply mitigation

↓

Validate recovery

---

# Related Topics

- Server Health Check
- High CPU Investigation
- Linux Processes
- Linux Logs
- Troubleshooting Methodology

---

# 💡 SRE Thinking

Experienced SREs do not assume that high memory utilization is a problem.

Instead, they investigate memory availability, swap usage, application behavior and kernel events before deciding whether intervention is required.