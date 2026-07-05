# Linux Common Mistakes

Common operational mistakes during Linux troubleshooting and incident response.

---

## Mistakes to Avoid

- Running commands on the wrong server or environment.
- Restarting a service before checking status and logs.
- Deleting files without confirming ownership and retention requirements.
- Using `kill -9` before trying graceful termination.
- Assuming high load always means CPU saturation.
- Ignoring disk, memory and service health while focusing only on the application.
- Running broad filesystem scans on busy production systems without understanding impact.

---

## Related Documents

- [Linux Troubleshooting Mindset](../concepts/07-troubleshooting.md)
- [Filesystem Concept](../concepts/02-filesystem.md)
- [Processes Concept](../concepts/03-processes.md)
