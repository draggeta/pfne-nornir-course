#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config, netmiko_send_command

# 3a. Create a script with a custom task that accepts a vlan_id and a vlan_name as arguments.
# Utilize the "netmiko_send_config" task-plugin to send the VLAN configuration to the "eos" and
# "nxos" hosts.


def gen_vlans_a(task, vlan_id, vlan_name):
    task.run(
        task=netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )


def main_a():

    vlan_id = "357"
    vlan_name = "my_vlan"

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="eos") | F(platform="nxos"))
    result = nr.run(task=gen_vlans_a, vlan_id=vlan_id, vlan_name=vlan_name)

    print_result(result)


# 3b. Within your custom task, add logic to see if the desired VLAN configuration already exists on
# each device.

# If the VLAN name and the VLAN ID already exist, then do NOT send the configuration commands.
# Instead just return a message indicating no changes are necessary. If the necessary configurations
# do not exist, then execute the configuration changes.


def gen_vlans_b(task, vlan_id, vlan_name):

    # Check current VLAN configuration
    multi_result = task.run(
        task=netmiko_send_command, command_string=f"show vlan brief | include {vlan_id}"
    )

    # Inspect results and return if already correct
    vlan_out = multi_result[0].result
    if vlan_out:
        existing_vlan_id = vlan_out.split()[0]
        existing_vlan_name = vlan_out.split()[1]
        if existing_vlan_id == vlan_id and existing_vlan_name == vlan_name:
            return "No changes: configuration already correct."

    # Configuration not correct - make changes
    task.run(
        task=netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )
    return "Configuration changed!"


def main_b():
    vlan_id = "357"
    vlan_name = "my_vlan"

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="eos") | F(platform="nxos"))
    result = nr.run(task=gen_vlans_b, vlan_id=vlan_id, vlan_name=vlan_name)

    print_result(result)


# 3c. Modify your custom task to return a Nornir Result object. Set the value of changed, failed,
# and result. These values should correspond to what happened in the custom task.


def gen_vlans_c(task, vlan_id, vlan_name):

    # Check current VLAN configuration
    multi_result = task.run(
        task=netmiko_send_command, command_string=f"show vlan brief | include {vlan_id}"
    )

    # Inspect results and return if already correct
    vlan_out = multi_result[0].result
    if vlan_out:
        existing_vlan_id = vlan_out.split()[0]
        existing_vlan_name = vlan_out.split()[1]
        if existing_vlan_id == vlan_id and existing_vlan_name == vlan_name:
            changed = False
            failed = False
            result = f"Vlan {vlan_id} with name {vlan_name} exists, nothing to do!"
            return Result(host=task.host, result=result, changed=changed, failed=failed)

    changed = True
    multi_result = task.run(
        task=netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )
    if (
        "%Invalid command" in multi_result[0].result
        or "% Invalid input" in multi_result[0].result
    ):
        failed = True
        result_msg = "An invalid configuration command was used."
    else:
        # Note task still could be marked at failed from the "netmiko_send_config"
        # execution i.e. at the MultiResult level.
        failed = False
        result_msg = f"Configured vlan {vlan_id} with name {vlan_name}!"

    return Result(host=task.host, result=result_msg, changed=changed, failed=failed)


def main_c():
    vlan_id = "357"
    vlan_name = "my_vlan"

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="eos") | F(platform="nxos"))
    result = nr.run(task=gen_vlans_c, vlan_id=vlan_id, vlan_name=vlan_name)

    print_result(result)


if __name__ == "__main__":
    main_a()
    main_b()
    main_c()
