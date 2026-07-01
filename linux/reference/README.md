# Linux Commands for SRE

## System
```bash
## System
hostname
uptime
whoami
uname -a

## Filesystem
pwd
ls -lah
df -h
du -sh *

## Memory
free -m

## Process
ps aux
top
htop

## Network
ip addr
ip route
ss -tulnp
ping
curl

## Logs
journalctl
tail -f /var/log/syslog
dmesg