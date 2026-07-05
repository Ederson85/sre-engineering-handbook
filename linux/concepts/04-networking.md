# 04 - Networking

## Why Networking Matters for SRE

Many incidents reported as "the server is down" are actually network path, DNS, routing, firewall, load balancer or dependency issues.

Linux networking knowledge helps an SRE separate local host problems from external connectivity problems.

---

## What to Check

- Network interfaces and assigned IP addresses.
- Default route and specific routes.
- Listening ports.
- Local service binding.
- DNS resolution.
- Connectivity to dependencies.

---

## Useful Commands

```bash
ip addr
ip route
ss -tuln
getent hosts <hostname>
ping <host>
curl -v http://<host>:<port>
```

---

## SRE Interpretation

Investigate from inside out:

1. Is the interface up?
2. Does the server have the expected IP address?
3. Is the route correct?
4. Is the service listening locally?
5. Does DNS resolve to the expected address?
6. Can the server reach its dependency?
7. Can clients reach the service through the expected path?

---

## Key Takeaway

Network troubleshooting is path validation. Confirm each hop and avoid assuming the application is broken before validating host networking.
