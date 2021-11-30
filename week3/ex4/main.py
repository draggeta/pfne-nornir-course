#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command

from pprint import pprint

# 4a. Create a "config.yaml" file that points to the hosts, groups and defaults inventory files in
# the ~/nornir_inventory directory. Your config.yaml file should be the following:

# ---
# inventory:
#   plugin: nornir.plugins.inventory.simple.SimpleInventory
#   options:
#     host_file: "~/nornir_inventory/hosts.yaml"
#     group_file: "~/nornir_inventory/groups.yaml"
#     defaults_file: "~/nornir_inventory/defaults.yaml"

# Create a Python script that creates a new Nornir object from inventory using the above config.yaml
# file.

nr = InitNornir(config_file="config.yaml")

# 4b. From your Nornir object in exercise4a, add a filter and select only the "eos" group. Using the
# "netmiko_send_command" task-plugin, execute "show interface status" command against this "eos"
# group. Ensure that you receive structured data back from Netmiko.

eos_dev = nr.filter(F(groups__contains="eos"))
eos_tasks = eos_dev.run(
    task=netmiko_send_command,
    command_string="show interface status",
    use_textfsm=True,
)

pprint(eos_tasks["arista1"][0].result)

# 4c. From the results in exercise4b, process the interface table for all of the devices and create
# a single final dictionary. The primary dictionary keys of this final dictionary should be the
# switch names. The switch name keys should point to an inner dictionary. The inner dictionary
# should have the interface names as keys and point to another internal dictionary. This last
# internal dictionary should have keys of "status" and "vlan". See the full dictionary structure
# below. Pretty print the output, your final dictionary should look similar to the following:

# {'arista1': {'Et1': {'status': 'connected', 'vlan': '1'},
#              'Et2': {'status': 'connected', 'vlan': '2'},
#              'Et3': {'status': 'connected', 'vlan': '3'},
#              'Et4': {'status': 'connected', 'vlan': '4'},
#              'Et5': {'status': 'connected', 'vlan': '5'},
#              'Et6': {'status': 'connected', 'vlan': '6'},
#              'Et7': {'status': 'connected', 'vlan': '7'}},

output = {}
for k, v in eos_tasks.items():
    infs = v[0].result
    output[k] = {}
    for inf in infs:
        port = inf["port"]
        status = inf["status"]
        vlan = inf["vlan"]
        output[k][port] = {"status": status, "vlan": vlan}

pprint(output)
