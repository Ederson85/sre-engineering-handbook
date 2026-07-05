# 03 - Processes

## Why Processes Matter for SRE

Most Linux incidents eventually involve a process: an application consuming CPU, a service leaking memory, a stuck worker, a zombie process or a daemon that failed to start.

Understanding processes helps an SRE connect operating system symptoms to the service causing them.

---

## What to Check

- Which processes consume the most CPU.
- Which processes consume the most memory.
- Process owner and command line.
- Parent and child process relationship.
- Process state.
- Whether the process is managed by systemd, a supervisor, container runtime or manual shell.

---

## Useful Commands

```bash
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
ps -fp <PID>
pstree -ap <PID>
top
```

---

## Process States

Common process states:

- `R`: running or runnable.
- `S`: sleeping.
- `D`: uninterruptible sleep, often related to I/O.
- `Z`: zombie.
- `T`: stopped.

---

## SRE Interpretation

Do not kill a process only because it is at the top of `top`. First understand:

- Is this expected workload?
- Is the process business-critical?
- Is there redundancy?
- Is it managed by systemd or another orchestrator?
- Would restarting it cause customer impact?

Prefer graceful actions such as service restart, traffic drain or `kill -15` before forceful termination.

---

## Key Takeaway

Processes are where system behavior becomes visible. Investigate ownership, impact and management method before taking action.
