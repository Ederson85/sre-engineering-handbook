# 06 - Systemd

## Why Systemd Matters for SRE

Systemd manages many Linux services in production environments. When an application, agent or infrastructure daemon fails, systemd is often the first place to validate service state and restart behavior.

---

## What to Check

- Failed units.
- Service status.
- Restart count and recent failures.
- Service logs.
- Unit file configuration.
- Whether the service is enabled at boot.

---

## Useful Commands

```bash
systemctl --failed
systemctl status <service-name>
journalctl -u <service-name> -n 100 --no-pager
systemctl is-enabled <service-name>
systemctl cat <service-name>
```

---

## SRE Interpretation

Restarting a service can restore availability, but it can also hide evidence. Before restarting, capture the current status and recent logs whenever possible.

Ask:

- Did the service fail once or is it flapping?
- Did failure start after deployment or configuration change?
- Is the service required for a customer-facing path?
- Is there redundancy?
- Does restart need approval during an active incident?

---

## Key Takeaway

Systemd gives both control and evidence. Use it to understand service lifecycle before applying mitigation.
