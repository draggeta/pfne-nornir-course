#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F

# 3a. Using an F-filter, create a Nornir object that is the hosts belonging to the role "AGG". Print
# the hosts that are contained in this new Nornir object.

nr = InitNornir(config_file="config.yaml")

role_filt = F(role__contains="AGG")
role = nr.filter(role_filt)
print(role.inventory.hosts)

# 3b. Using an F-filter, create a Nornir object of devices that are members of either the "sea" or
# (union) the "sfo" group. Print the hosts that are contained in this new Nornir object.

grp1_filt = F(groups__contains="sea")
grp2_filt = F(groups__contains="sfo")
grp = nr.filter(grp1_filt | grp2_filt)
print(grp.inventory.hosts)

# 3c. Using an F-filter, create a Nornir object that contains devices that belong to the "WAN" role
# and (intersection) have a WIFI password of "racecar". Note, for a nested dictionary key inside
# data, you can use the following pattern:

# F(site_details__wifi_password__contains="whatever")

# Where the corresponding section of inventory is:
# data:
#   site_details:
#     wifi_password: whatever

role_filt = F(role__contains="WAN")
wp_filt = F(site_details__wifi_password__contains="racecar")
dev = nr.filter(role_filt & wp_filt)
print(dev.inventory.hosts)

# 3d. Modify the filter from exerice3c such that you retrieve the devices that do NOT have a wifi
# password of "racecar

dev2 = nr.filter(role_filt & ~wp_filt)
print(dev2.inventory.hosts)
