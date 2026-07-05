# 05 - Logs

## Why Logs Matter for SRE

Logs provide the timeline of what the system and applications observed. During incidents, they help confirm symptoms, identify errors and correlate events with deployments, restarts or infrastructure changes.

---

## What to Check

- Recent system warnings and errors.
- Service-specific logs.
- Kernel messages.
- Authentication or permission failures.
- Repeated errors that indicate loops or retries.
- Timestamp correlation with monitoring alerts.

---

## Useful Commands

```bash
journalctl -p warning -n 100 --no-pager
journalctl -u <service-name> -n 100 --no-pager
dmesg -T | tail -n 100
tail -n 100 /var/log/syslog
tail -f /var/log/syslog
```

---

## SRE Interpretation

Logs should be used as evidence, not as the only source of truth. A useful investigation correlates logs with metrics, traces, deployments, configuration changes and user impact.

When reviewing logs, look for:

- First error before the alert.
- Error rate increasing over time.
- Dependency failures.
- Out-of-memory messages.
- Disk or I/O errors.
- Service restarts.

---

## Key Takeaway

Logs explain what happened from the system perspective. The best SRE investigations combine logs with metrics and a clear incident timeline.
