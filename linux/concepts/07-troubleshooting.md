# 07 - Troubleshooting

## Linux Troubleshooting Mindset

Good Linux troubleshooting is structured, evidence-based and careful with production impact.

During an incident, an SRE should reduce uncertainty step by step instead of jumping directly to a restart or configuration change.

---

## Investigation Flow

```text
Confirm target server
        |
Understand the symptom
        |
Check system health
        |
Inspect CPU, memory and disk
        |
Review processes and services
        |
Validate network path
        |
Read relevant logs
        |
Decide mitigation or escalation
```

---

## Principles

- Confirm the environment before running operational commands.
- Prefer read-only commands during diagnosis.
- Capture evidence before mitigation.
- Separate symptoms from root cause.
- Validate customer impact, not only server metrics.
- Escalate when the affected component owner or business risk is unclear.
- Document actions and timestamps.

---

## Common Mistakes

- Restarting services before checking logs.
- Deleting files without confirming ownership.
- Using `kill -9` as the first action.
- Assuming high load always means high CPU.
- Troubleshooting the application before checking disk, memory and service health.
- Ignoring recent deployments or configuration changes.

---

## Key Takeaway

Troubleshooting is a decision process. Commands collect evidence, but SRE judgment determines the safest next action.
