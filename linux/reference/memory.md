# Memory Commands

**Module:** Linux  
**Category:** Reference  
**Level:** Beginner

---

# Overview

Memory analysis is one of the first steps during performance investigations.

An SRE should determine whether the operating system is experiencing memory pressure before analyzing the application itself.

---

# free

## Purpose

Displays memory usage.

```bash
free -m
```

---

# vmstat

## Purpose

Displays virtual memory statistics.

```bash
vmstat 1 5
```

---

# top

## Purpose

Displays real-time CPU and memory utilization.

```bash
top
```

---

# What to Check

- Available memory
- Swap usage
- High memory consumers
- Memory pressure

---

# Next Step

Continue with **Filesystem Commands**.