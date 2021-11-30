#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F

# 2a. Using the inventory files from the previous exercise, create a Nornir object that is filtered
# to only "arista1". Use the .filter() method to accomplish this. Print the hosts that are contained
#  in this new Nornir object.
nr = InitNornir(config_file="config.yaml")

a1 = nr.filter(name="arista1")
print(a1.inventory.hosts)

# 2b. Using the filter method, create a Nornir object that is filtered to all devices using the role
# "WAN". Print the hosts that are contained in this new Nornir object. Further filter on this newly
# created Nornir object to capture only hosts using port 22. Once again, print the hosts in this new
# Nornir object.

wan = nr.filter(role="WAN")
print(wan.inventory.hosts)

wan_port = wan.filter(port=22)
print(wan_port.inventory.hosts)


# 2c. Using an F-filter, create a new Nornir object that contains all the hosts that belong to the
# "sfo" group. Print the hosts that are contained in this new Nornir object.

filt = F(groups__contains="sfo")
grp_filt = nr.filter(filt)

print(grp_filt.inventory.hosts)
