# Real World - Connected to the Wrong Server

**Module:** Linux  
**Category:** Real World

---

# Scenario

During a production incident, an engineer connected to a server believing it was the production environment.

Before executing any maintenance task, the engineer verified the hostname.

```bash
hostname
```

The result revealed that the session was connected to the staging environment.

---

# Lesson Learned

Always verify the target server before executing operational commands.

Simple validation steps can prevent production incidents.

---

# Commands Used

```bash
hostname
whoami
```

---

# Key Takeaway

Never assume.

Always verify.