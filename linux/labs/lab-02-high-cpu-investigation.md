# Lab 02 - High CPU Investigation

**Module:** Linux  
**Category:** Lab  
**Level:** Intermediate  
**Estimated Time:** 20 minutes

---

# Objective

Investigate a High CPU alert using a structured SRE investigation workflow.

The goal is to identify the root cause before applying any mitigation.

---

# Scenario

A monitoring platform reports that CPU utilization has remained above **95%** for the last 10 minutes.

Users are reporting:

- Slow application response
- Request timeouts
- Increased latency

You have SSH access to the server.

Your mission is to investigate the issue before taking any action.

---

# Prerequisites

- Linux VM or Lab Environment
- Terminal access
- Basic Linux knowledge

> ⚠️ Do not execute mitigation commands in a production environment without following your organization's change management process.

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
- Is the Load Average abnormal?

---

## Task 2 — Check CPU Utilization

Execute:

```bash
top
```

Observe:

- CPU utilization
- Idle CPU
- Running processes

---

## Task 3 — Identify CPU Consumers

Execute:

```bash
ps aux --sort=-%cpu | head
```

Questions:

- Which process consumes the most CPU?
- Is this expected?

---

## Task 4 — Inspect the Process

Execute:

```bash
ps -fp <PID>
```

If necessary:

```bash
lsof -p <PID>
```

Understand what the process is doing.

---

## Task 5 — Review Logs

If the application uses systemd:

```bash
journalctl -u <service-name> -n 100 --no-pager
```

Look for:

- Exceptions
- Restart loops
- Unexpected errors

---

## Task 6 — Validate Recent Changes

Ask:

- Was there a deployment?
- Was configuration changed?
- Has traffic increased?
- Is there any scheduled batch job?

---

# Expected Result

By the end of this lab you should be able to answer:

- What caused the High CPU alert?
- Which process is responsible?
- Is the application healthy?
- Is mitigation required?
- Can the incident be safely escalated?

---

# Lessons Learned

High CPU investigation is an evidence collection exercise.

Never terminate a process without understanding:

- what it is;
- who owns it;
- why it is consuming CPU.

---

# 💡 SRE Thinking

High CPU is often only the visible symptom.

Experienced SREs investigate before acting.

Every command executed should answer a question.

Evidence first.

Mitigation second.

Learning always.