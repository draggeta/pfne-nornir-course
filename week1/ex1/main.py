#!/usr/bin/env python

from nornir import InitNornir

# Create a Nornir object
nr = InitNornir()

# Look at nr.inventory
print(nr.inventory)

# Look at nr.inventory.hosts
print(nr.inventory.hosts)

# Look at nr.inventory.hosts['tfr-work']
print(nr.inventory.hosts["tfr-work"])

# Look at nr.inventory.hosts['tfr-work'].hostname
print(nr.inventory.hosts["tfr-work"].hostname)
