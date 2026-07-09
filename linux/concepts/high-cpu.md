# High CPU

**Module:** Linux  
**Category:** Concept  
**Level:** Beginner  
**Estimated Reading Time:** 5 minutes

---

## Overview

High CPU occurs when one or more processes consume a large amount of processor resources for a sustained period.

For Site Reliability Engineers, high CPU is important because it can increase application latency, cause request timeouts and reduce the stability of services running on the server.

---

## Why It Matters

A server with sustained high CPU may experience:

- Slow application response
- Increased request latency
- Failed health checks
- Process starvation
- Service degradation

High CPU should not be treated as a root cause immediately. It is a symptom that requires investigation.

---

## Common Causes

Common causes of high CPU include:

- Application bugs
- Inefficient queries or loops
- Traffic spikes
- Background jobs
- Misconfigured services
- Deployment regressions
- Malware or unexpected processes

---

## Investigation Workflow

```text
Confirm server identity
        ↓
Check load average
        ↓
Check real-time CPU usage
        ↓
Identify top CPU consumers
        ↓
Validate process details
        ↓
Check logs and recent changes
        ↓
Mitigate safely
        ↓
Validate recovery