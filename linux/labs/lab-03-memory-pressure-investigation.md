# Lab 03 - Memory Pressure Investigation

**Module:** Linux  
**Category:** Lab  
**Level:** Intermediate  
**Estimated Time:** 25 minutes

---

# Objective

Investigate a Memory Pressure alert using a structured SRE investigation workflow.

The objective is to determine whether the issue is caused by application behavior, infrastructure limitations or memory leaks before applying mitigation.

---

# Scenario

A monitoring platform reports that memory utilization has remained above **92%** for the last 15 minutes.

Users report:

- Slow application response
- Increased latency
- Occasional application restarts

Monitoring also indicates swap activity.

You have SSH access to the server.

Your mission is to investigate the incident before taking any corrective action.

---

# Prerequisites

- Linux VM or Lab Environment
- Terminal access
- Basic Linux knowledge

> ⚠️ Never execute mitigation commands directly in a production environment without following your organization's operational procedures.

---

# Tasks

## Task 1 — Confirm the Server

Execute:

```bash
hostname
whoami
uptime
```

Questions:

- Am I connected to the correct server?
- Is the system responsive?

---

## Task 2 — Check Memory Usage

Execute:

```bash
free -h
```

Observe:

- Available memory
- Used memory
- Swap usage

Question:

Is the system really under Memory Pressure?

---

## Task 3 — Identify Memory Consumers

Execute:

```bash
ps aux --sort=-%mem | head
```

Questions:

- Which process is consuming the most memory?
- Is this expected?

---

## Task 4 — Monitor the System

Execute:

```bash
top
```

or

```bash
htop
```

Observe:

- RES memory
- Swap usage
- CPU correlation

---

## Task 5 — Check Kernel Information

Execute:

```bash
cat /proc/meminfo
```

Focus on:

- MemAvailable
- Cached
- Buffers
- SwapFree

---

## Task 6 — Verify OOM Events

Execute:

```bash
dmesg | grep -i oom
```

or

```bash
journalctl -k | grep -i oom
```

Questions:

- Has the kernel terminated any process?
- When did it happen?

---

## Task 7 — Review Logs

Execute:

```bash
journalctl -u <service-name> -n 100 --no-pager
```

Look for:

- Memory allocation failures
- Exceptions
- Restart loops

---

## Task 8 — Validate Recent Changes

Confirm:

- Recent deployments
- Configuration changes
- Traffic spikes
- Scheduled jobs

---

# Expected Result

At the end of this lab you should be able to answer:

- Is Memory Pressure occurring?
- Which process is responsible?
- Did the OOM Killer execute?
- Is mitigation required?
- Can the service safely continue operating?

---

# Lessons Learned

High memory utilization alone does not indicate a problem.

Always evaluate:

- Available memory
- Swap activity
- OOM events
- Application behavior

---

# 💡 SRE Thinking

Good SREs do not investigate symptoms in isolation.

Memory Pressure must always be correlated with application behavior, kernel events and recent operational changes.

Collect evidence first.

Mitigate only after understanding the root cause.