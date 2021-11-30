#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command

# Create a Nornir object
nr = InitNornir(config_file="config.yaml")

# 3. Using the Nornir filter pattern shown below and the 'netmiko_send_command'
# task-plugin capture the output of 'show ip arp' from all of the Cisco-IOS and
# Arista-EOS devices.

ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")

nr = nr.filter(ios_filt | eos_filt)

# Process the "show ip arp" results such that only the default gateway is
# retained from the ARP table. Note, please accomplish this exercise by
# handling the AggregatedResult and MultiResult in your Python program instead
# of using a router CLI command
# (i.e. do not do "show ip arp | include gateway"). In other words, the purpose
#  of this exercise is for you to gain familiarity with handling Nornir result
#  objects.

# For both exercise3 and exercise4, you can just hard-code the gateway value
# into your code. In other words, you do not need to dynamically determine the
# default gateway.

# Print output similar to the following to standard output (the "Host" should
# be the Nornir host that you retrieved the ARP data from; the "Gateway" should
# be the "show ip arp" gateway entry from that Host). Note, the IP address of
# the default gateway and its corresponding MAC address might be different in
# your lab environment.

# Host: cisco3, Gateway: Internet 10.220.88.1 8 0062.ec29.70fe ARPA GigabitEthernet0/0/0
# Host: cisco4, Gateway: Internet 10.220.88.1 8 0062.ec29.70fe ARPA GigabitEthernet0/0/0
# Host: arista1, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
# Host: arista2, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
# Host: arista3, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
# Host: arista4, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1

my_results = nr.run(task=netmiko_send_command, command_string="show ip arp")

for host, results in my_results.items():
    for result in results:
        for line in result.result.split("\n"):
            if "10.220.88.1" in line:
                print(f"Host: {host}, Gateway: {line}")
