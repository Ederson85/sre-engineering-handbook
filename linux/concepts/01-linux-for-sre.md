# 01 - Linux for SRE

## Why Linux matters for SRE

Linux is the foundation of many production environments.

A Site Reliability Engineer needs to understand Linux not only to run commands, but to investigate system behavior, identify bottlenecks and support reliable services.

In real incidents, Linux knowledge helps answer questions such as:

- Is the server healthy?
- Is CPU usage abnormal?
- Is memory under pressure?
- Is the filesystem full?
- Is the application process running?
- Are services failing?
- Are logs showing errors?
- Is there a network issue?

---

## SRE Mindset

Linux troubleshooting is not about memorizing commands.

It is about following a structured investigation process:

1. Understand the symptom
2. Check system health
3. Validate resources
4. Inspect processes
5. Review logs
6. Confirm network behavior
7. Identify the root cause
8. Document the learning

---

## First Commands
```bash
hostname
uptime
whoami
pwd
ls
df -h
free -m
top
ps aux