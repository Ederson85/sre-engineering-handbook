# Linux SRE Cheatsheet

## Quick Health Check

```bash
uptime
df -h
free -m
top
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head

## Disk Investigation
df -h
du -sh *

## Process Investigation
ps aux
top

## Network Investigation
ip addr
ip route
ss -tulnp

## Logs
journalctl -xe
dmesg
tail -f /var/log/syslog