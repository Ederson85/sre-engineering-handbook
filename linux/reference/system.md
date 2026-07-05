# System Commands

**Module:** Linux  
**Category:** Reference  
**Level:** Beginner

---

# Overview

System commands provide basic information about the current Linux host.

These commands are typically the first executed by an SRE after connecting to a server.

Their purpose is to quickly identify the environment before investigating applications or services.

---

# hostname

## Purpose

Displays the current hostname.

```bash
hostname
```

Example:

```text
prd-api-01
```

---

# whoami

## Purpose

Displays the current logged-in user.

```bash
whoami
```

Example:

```text
root
```

---

# uptime

## Purpose

Displays system uptime and current load averages.

```bash
uptime
```

Example:

```text
10:42:31 up 37 days, 2 users, load average: 0.25, 0.31, 0.28
```

---

# uname

## Purpose

Displays kernel and operating system information.

```bash
uname -a
```

---

# Why These Commands Matter

Before analyzing CPU, memory or logs, an SRE must confirm:

- Which server is being accessed
- Which user is connected
- How long the server has been running
- Which operating system and kernel version are in use

This basic validation reduces operational mistakes and accelerates incident response.

---

# Next Step

Continue with [Memory Commands](memory.md).
