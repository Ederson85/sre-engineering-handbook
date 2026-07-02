# Lab 01 - Server Health Check

**Module:** Linux  
**Category:** Lab  
**Level:** Beginner  
**Estimated Time:** 15 minutes

---

## Objective

Perform a basic Linux server health check using commands commonly used by SREs during incident investigation.

---

## Scenario

A monitoring alert reports that a Linux server is responding slowly.

Before restarting services or escalating the incident, your goal is to collect evidence about the current state of the server.

---

## Tasks

### 1. Identify the server
```bash
hostname
whoami
uname -a
```

### 2. Check uptime and load
```bash
uptime
```
Observe
- Load Average

### 3. Check memory
```bash
free -m
vmstat 1 5
```
Expected
- Available memory should not be critically low.
- Swap usage should normally remain close to zero.

### 4. Check filesystem usage
```bash
df -h
lsblk
```
Expected
- Production filesystems should generally remain below 80% utilization.

### 5. Check top processes
```bash
top
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```
Observe
- A consistently high load average may indicate CPU contention.
- Use `top` or `ps` to determine whether the bottleneck is CPU, memory or running processes.

### 6. Check network basics
```bash
ip addr
ip route
```

## Expected Result
At the end of this lab, you should be able to answer:
- Is the server overloaded?
- Is memory under pressure?
- Is any filesystem close to full?
- Are there abnormal processes consuming CPU or memory?
- Is the network interface available?

## Lessons Learned
A server health check helps SREs avoid assumptions and collect evidence before taking action during an incident.