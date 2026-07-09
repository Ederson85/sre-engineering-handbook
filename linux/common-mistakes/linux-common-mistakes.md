# Linux Common Mistakes

**Module:** Linux  
**Category:** Common Mistakes

---

## Overview

Many production incidents become worse because engineers take action before understanding the problem.

This guide highlights common mistakes and the recommended SRE approach.

---

| ❌ Common Mistake | ✅ Better Practice |
|------------------|-------------------|
| Restart the service immediately | Investigate the root cause first |
| Use `kill -9` as the first option | Use `kill -15` whenever possible |
| Ignore system logs | Review logs before taking action |
| Reboot the server without evidence | Collect evidence before rebooting |
| Delete files to free disk space | Identify the root cause of disk growth |
| Ignore Load Average | Correlate Load Average with CPU utilization |
| Troubleshoot only the infrastructure | Correlate infrastructure and application metrics |
| Execute commands directly in production | Validate in a lab or non-production environment whenever possible |
| Assume the last deployment is the problem | Confirm the timeline with evidence |
| Finish the incident without documentation | Record timeline, root cause and lessons learned |

---

# 💡 SRE Thinking

Good SREs do not react impulsively.

They investigate, validate and then act.

The safest action is not always the fastest one.