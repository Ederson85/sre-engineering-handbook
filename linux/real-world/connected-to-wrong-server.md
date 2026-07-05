# Real World - Connected to the Wrong Server

**Module:** Linux  
**Category:** Real World

---

## Scenario

During a production incident, an engineer connected to a server believing it was the production environment.

Before executing any maintenance task, the engineer verified the hostname.

```bash
hostname
```

The result revealed that the session was connected to the staging environment.

---

## Lesson Learned

Always verify the target server before executing operational commands.

Simple validation steps can prevent production incidents.

In regulated or high-risk environments, this check should be part of the standard operating procedure before any restart, cleanup, permission change or deployment action.

---

## Commands Used

```bash
hostname
whoami
pwd
uname -a
```

---

## Preventive Controls

- Use clear hostnames that include environment and service.
- Display environment information in the shell prompt.
- Require change or incident context before production actions.
- Prefer read-only validation commands before mitigation.
- Document the server name in the incident timeline.

---

## Key Takeaway

Never assume.

Always verify.
