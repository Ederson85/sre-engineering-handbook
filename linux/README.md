# Linux for SRE

Linux is one of the core foundations for Site Reliability Engineering.

This module focuses on practical Linux knowledge used in real production environments, including system analysis, troubleshooting, processes, logs, networking and service management.


---

## Structure

```text
linux/
├── concepts/
├── reference/
├── labs/
├── troubleshooting/
├── real-world/
├── best-practices/
├── common-mistakes/
├── cheatsheets/
├── diagrams/
├── images/
└── runbooks/
```

---

## Contents

- [01 - Linux for SRE](concepts/01-linux-for-sre.md)
- [02 - Filesystem](concepts/02-filesystem.md)
- [03 - Processes](concepts/03-processes.md)
- [04 - Networking](concepts/04-networking.md)
- [05 - Logs](concepts/05-logs.md)
- [06 - Systemd](concepts/06-systemd.md)
- [07 - Troubleshooting](concepts/07-troubleshooting.md)
- [Server Health Check Concept](concepts/server-health.md)
- [Reference](reference/README.md)
- [Cheatsheet](cheatsheets/README.md)
- [Server Health Check Troubleshooting](troubleshooting/server-health-check.md)
- [Server Health Check Runbook](runbooks/server-health-check.md)

---

## Labs

- [Lab 01 - Server Health Check](labs/lab-01-server-health-check.md)

---

## Status

The Linux foundation sprint is usable for review and practice.

Next improvements:

- Add advanced runbooks for high CPU, memory pressure and filesystem exhaustion.
- Expand references with process, network, log and systemd commands.
- Add safer lab environments using containers or disposable virtual machines.
