#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

# 1a. Copy the hosts.yaml and groups.yaml files from ~/nornir_inventory into your working directory.
# Create a "config.yaml" file that points to the copied hosts.yaml and groups.yaml files.  The
# config.yaml file should still reference the "defaults.yaml" file in ~/nornir_inventory.

# 1b. Add a "data" field to both the "cisco3" and "cisco4" hosts (in hosts.yaml). Inside of this
# "data" field add a key named "snmp_id" with a corresponding value that you select. Add a "data"
# field into the "eos" group in groups.yaml. Once again, inside of this "data" field add a key named
# "snmp_id" with a corresponding value that you select.

# 1c. Write a custom task that uses the netmiko_send_config task-plugin to configure the SNMP chassis
# ID for all of the Cisco IOS and Arista EOS devices. For the IOS devices use the "snmp_id" value in
# hosts.yaml. For the EOS devices, configure the chassis ID to be the "snmp_id" attribute plus the
# name of the device (Nornir inventory name). The EOS devices should be pulling the base snmp_id
# attribute from groups.yaml.

# The syntax for the Cisco IOS devices is as follows:
#   snmp-server chassis-id YOURSTRING
#
# And for the Arista EOS devices:
#   snmp chassis-id YOURSTRING-name


def config_snmp(task):
    host = task.host
    platform = task.host.platform
    snmp_str = {
        "ios": f"snmp-server chassis-id {host['snmp_id']}",
        "eos": f"snmp chassis-id {host['snmp_id']}-{host.name}",
    }

    task.run(task=netmiko_send_config, config_commands=f"{snmp_str[platform]}")


def main():
    nr = InitNornir(config_file="config.yaml")

    nr = nr.filter(F(platform="ios") | F(platform="eos"))

    res = nr.run(task=config_snmp)

    print_result(res)


if __name__ == "__main__":
    main()
