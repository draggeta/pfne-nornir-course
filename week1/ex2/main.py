#!/usr/bin/env python

from nornir import InitNornir

# Create a Nornir object
nr = InitNornir()

hosts = nr.inventory.hosts

for host in hosts:
    print(
        f"\n\nhost    : {host}\n",
        f"{'-'*20}\n",
        f"hostname: {hosts[host].hostname}\n",
        f"groups  : {hosts[host].groups}\n",
        f"platform: {hosts[host].platform}\n",
        f"username: {hosts[host].username}\n",
        f"password: {hosts[host].password}\n",
        f"port    : {hosts[host].port}\n",
    )
