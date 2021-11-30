#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get

# Create a Nornir object
nr = InitNornir(config_file="config.yaml")

# 4. Using a NAPALM getter instead of Netmiko, capture the ARP table output
# from all of the EOS and IOS devices. The NAPALM "arp_table" getter will
# return a list of dictionaries. In this list of dictionaries each
# inner-dictionary will correspond to one entry in the ARP table

ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")

nr = nr.filter(ios_filt | eos_filt)

# Post-process the data retrieved from this NAPALM getter and print out the
# "host" name (for example, "cisco3", "cisco4") and the NAPALM inner dictionary
#  corresponding to the MAC address of the default gateway. For both exercise3
# and exercise4, you can just hard-code the gateway value into your code. In
# other words, you do not need to dynamically determine the default gateway.

# Your printed output should be similar to the following (note, the default
# gateway and MAC address in your lab environment might be different).

# Host: cisco3, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 5.0}
# Host: cisco4, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 5.0}
# Host: arista1, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
# Host: arista2, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
# Host: arista3, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
# Host: arista4, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}

my_results = nr.run(task=napalm_get, getters=["arp_table"])

for host, results in my_results.items():
    for result in results:
        for line in result.result["arp_table"]:
            if line["ip"] != "10.220.88.1":
                continue
            print(f"Host: {host}, Gateway: {line}")
