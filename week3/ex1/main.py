#!/usr/bin/env python

from nornir import InitNornir

# 1a. Create a Python script that initializes a Nornir object. Print out the "data" attribute of the
# "arista3" host. Call the "items()" method on host "arista3". Notice that when calling the items()
# method that Nornir not only displays the "data" entries associated at the host-level, but also
# recurses the data for the groups (that the host belongs to).
nr = InitNornir(config_file="config.yaml")
print(nr.inventory.hosts["arista3"].data)
print(nr.inventory.hosts["arista3"].items())


# 1b. In the "sea" group in groups.yaml, add a "timezone" key and set the value to "PST". Print out
# the timezone for each of the hosts in the inventory. Without setting any data fields on the
# "arista3" host, modify the inventory files such that the timezone attribute for "arista3" is set
# to "PST".
nr = InitNornir(config_file="config.yaml")

for host in nr.inventory.hosts:
    print(nr.inventory.hosts[host]["timezone"])

# move the group order around for arista3
