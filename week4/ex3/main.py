#!/usr/bin/env python

from nornir import InitNornir

# 3a. Create a script with a custom task that accepts a vlan_id and a vlan_name as arguments.
# Utilize the "netmiko_send_config" task-plugin to send the VLAN configuration to the "eos" and
# "nxos" hosts.

# 3b. Within your custom task, add logic to see if the desired VLAN configuration already exists on
# each device.

# If the VLAN name and the VLAN ID already exist, then do NOT send the configuration commands.
# Instead just return a message indicating no changes are necessary. If the necessary configurations
# do not exist, then execute the configuration changes.

# 3c. Modify your custom task to return a Nornir Result object. Set the value of changed, failed,
# and result. These values should correspond to what happened in the custom task.
