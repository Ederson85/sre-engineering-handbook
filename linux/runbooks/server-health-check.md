# Server Health Check Runbook

**Module:** Linux  
**Category:** Runbook  
**Level:** Beginner  
**Use Case:** Initial mitigation during Linux server health incidents

---

## Alert

A Linux server is reported as slow, unstable or partially unresponsive.

Common alert sources:

- Monitoring platform
- User report
- Application timeout
- High response time
- Infrastructure alert

---

## Impact

Potential impact may include:

- Increased application latency
- Failed requests
- Service degradation
- Application instability
- User-facing errors

---

## Prerequisites

Before applying any mitigation action:

- Confirm the correct server.
- Confirm the environment: production, staging or development.
- Check if there is an active incident.
- Check if the service has redundancy.
- Avoid destructive actions without validation.
- Prefer graceful mitigation before forceful actions.

---

## Diagnosis

### Step 1 — Confirm server identity

```bash
hostname
whoami
```

Confirm you are connected to the expected server and using the expected user.

---

### Step 2 — Check system load

```bash
uptime
```

If Load Average is high, continue with CPU and process validation.

---

### Step 3 — Check CPU and processes

```bash
top
ps aux --sort=-%cpu | head
```

Identify processes consuming abnormal CPU.

---

### Step 4 — Check memory

```bash
free -m
vmstat 1 5 5
ps aux --sort=-%mem | head
```

Identify memory pressure, swap usage or abnormal memory consumers.

---

### Step 5 — Check filesystem

```bash
df -hT
du -xhd1 / 2>/dev/null | sort -h
```

Identify filesystems above safe utilization thresholds.

---

### Step 6 — Check services and logs

```bash
systemctl --failed
journalctl -p warning -n 100 --no-pager
dmesg -T | tail -n 100
```

Identify failing services or system-level errors.

---

## Mitigation

### Scenario 1 — Process consuming excessive CPU

#### 1. Identify the process

```bash
ps aux --sort=-%cpu | head
```

Example:

```text
appuser   3245  99.8  4.1 123456 78900 ?  Sl  10:10  25:32 java -jar app.jar
```

#### 2. Validate process details

```bash
ps -fp <PID>
```

Example:

```bash
ps -fp 3245
```

#### 3. Check open files and ports

```bash
lsof -p <PID>
ss -tulnp | grep <PID>
```

#### 4. Prefer graceful stop

If the process is managed by systemd:

```bash
systemctl status <service-name>
systemctl stop <service-name>
```

If the process is not managed by systemd:

```bash
kill -15 <PID>
```

#### 5. Force termination only as last resort

```bash
kill -9 <PID>
```

Use `kill -9` only when graceful termination fails and the impact is confirmed.

#### 6. Validate recovery

```bash
uptime
top
ps aux --sort=-%cpu | head
```

---

### Scenario 2 — Memory pressure

#### 1. Confirm memory condition

```bash
free -m
vmstat 1 5 5
ps aux --sort=-%mem | head
```

#### 2. Identify the top memory consumer

```bash
ps aux --sort=-%mem | head
```

#### 3. Validate process

```bash
ps -fp <PID>
```

#### 4. Restart service gracefully when safe

```bash
systemctl status <service-name>
systemctl restart <service-name>
```

#### 5. Validate memory recovery

```bash
free -m
vmstat 1 5 5
```

---

### Scenario 3 — Filesystem close to full

#### 1. Confirm disk usage

```bash
df -h
```

#### 2. Identify large directories

```bash
du -xhd1 / 2>/dev/null | sort -h
```

#### 3. Investigate logs

```bash
du -sh /var/log/* 2>/dev/null | sort -h
```

#### 4. Clean only safe files

Preview files before deleting anything:

```bash
find /tmp -xdev -type f -mtime +7 -print
```

Examples of controlled cleanup:

```bash
journalctl --vacuum-time=7d
```

```bash
find /tmp -xdev -type f -mtime +7 -delete
```

Do not delete application files without validation.

#### 5. Validate disk recovery

```bash
df -h
```

---

### Scenario 4 — Failed systemd service

#### 1. List failed services

```bash
systemctl --failed
```

#### 2. Inspect service

```bash
systemctl status <service-name>
journalctl -u <service-name> -n 100 --no-pager
```

#### 3. Restart service when safe

```bash
systemctl restart <service-name>
```

#### 4. Validate status

```bash
systemctl status <service-name>
```

---

## Validation

After mitigation, validate:

```bash
uptime
free -m
df -h
top
systemctl --failed
```

Confirm:

- Load Average returned to expected levels.
- Memory is stable.
- Filesystems have available capacity.
- Critical services are running.
- Application behavior improved.

---

## Rollback

If mitigation causes unexpected impact:

- Start the stopped service again.
- Restore previous configuration if changed.
- Escalate to the application or infrastructure owner.
- Document the action and timeline.

Useful commands:

```bash
systemctl start <service-name>
systemctl restart <service-name>
```

---

## Escalation

Escalate when:

- The affected process is business-critical.
- The service cannot be restarted safely.
- Disk cleanup requires application knowledge.
- The server remains unstable after mitigation.
- The root cause is unclear.
- Customer impact continues.

---

## Post-Incident Actions

After recovery:

- Document the timeline.
- Identify the root cause.
- Create or update monitoring alerts.
- Review capacity thresholds.
- Create preventive automation when possible.
- Update this runbook if new learnings were found.

---

## Related Documents

- [Server Health Check Concept](../concepts/server-health.md)
- [System Reference](../reference/system.md)
- [Memory Reference](../reference/memory.md)
- [Filesystem Reference](../reference/filesystem.md)
- [Lab 01 - Server Health Check](../labs/lab-01-server-health-check.md)
- [Server Health Check Troubleshooting](../troubleshooting/server-health-check.md)
- [Linux SRE Cheatsheet](../cheatsheets/README.md)
