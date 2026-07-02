# Server Health Check

**Module:** Linux  
**Category:** Concepts  
**Level:** Beginner  
**Estimated Reading Time:** 5 minutes

---

# Overview

A Server Health Check is the first assessment performed by a Site Reliability Engineer after connecting to a Linux server.

Its purpose is to determine whether the operating system is healthy before investigating a specific application or service.

Instead of making assumptions, SREs collect evidence about the current state of the server.

---

# Why It Matters

A healthy application depends on a healthy operating system.

Many production incidents are caused by infrastructure issues such as:

- CPU saturation
- Memory pressure
- Disk exhaustion
- Network failures
- Service failures

Identifying these conditions early reduces troubleshooting time and improves incident response.

---

# Health Check Areas

A standard Linux health check evaluates:

- Host identification
- System uptime
- CPU utilization
- Memory utilization
- Filesystem usage
- Running processes
- System services
- Network connectivity
- System logs

---

# Investigation Workflow

```text
Connect to the server
        ↓
Confirm host identity
        ↓
Check uptime
        ↓
Analyze CPU
        ↓
Analyze memory
        ↓
Check disk usage
        ↓
Inspect running processes
        ↓
Verify services
        ↓
Review logs
        ↓
Continue application troubleshooting
```

---

# Key Takeaway

A Server Health Check is not intended to solve an incident.

Its objective is to quickly understand the overall condition of the operating system before moving to deeper investigation.