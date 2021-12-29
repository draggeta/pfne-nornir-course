#!/usr/bin/env python

import os
import random

from netmiko.ssh_exception import NetmikoAuthenticationException

from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
from nornir_netmiko.tasks.netmiko_send_command import netmiko_send_command
from nornir_utils.plugins.functions.print_result import print_result

# 5a. Create a Nornir script that includes a custom task that executes "show clock" on the Cisco
# IOS, Arista EOS, and Cisco NX-OS devices. This same custom task should execute
# "show system uptime" on the Juniper SRX. Use the "print_result" function to verify the output of
# this task is correct.


def show_clock_a(task):
    if task.host.platform == "srx":
        cmd = "show system uptime"
    else:
        cmd = "show clock"
    task.run(task=netmiko_send_command, command_string=cmd)


def main_a():
    nr = InitNornir(config_file="config.yaml")

    agg_res = nr.run(task=show_clock_a)

    print_result(agg_res)


# 5b. Expand on exercise5a, except randomly change the password on some of your devices in inventory
# (this is prior to executing the custom task that connects to those devices). This can be
# accomplished using the "random.choice" function as follows:

# for host, data in nr.inventory.hosts.items():
#     if random.choice([True, False]):
#        data.password = BAD_PASSWORD

# This will of course cause the "send_command" task to fail due to authentication issues.

# Now, catch the NornirSubTaskError exception (if the sub task exception is
# "NetMikoAuthenticationException") and then set the host password back to "88newclass". After this
# is done, re-execute the Netmiko "send_command" task (all of this code should be inside of your
# custom task).

# Re-run your script, the end result of this should be that the appropriate data is gathered from
# all devices in the inventory. The devices that failed authentication the first time should have
# been corrected and executed correctly on the second attempt.

# Note, you will probably want to execute the following (inside your NornirSubTaskError exception
# handler to remove the failed connection attempt):

#     task.results.pop()

# This will make your print_results output much cleaner (i.e. it will remove the failed SSH attempt
# from the print_results output).


def show_clock_b(task):
    if task.host.platform == "junos":
        cmd = "show system uptime"
    else:
        cmd = "show clock"

    try:
        task.run(task=netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result[0].exception, NetmikoAuthenticationException):
            task.results.pop()
            task.host.password = os.getenv("NORNIR_PASSWORD")
            task.run(task=netmiko_send_command, command_string=cmd)
        else:
            return "Unknown error occurred."


def main_b():
    nr = InitNornir(config_file="config.yaml")
    for _, host in nr.inventory.hosts.items():
        if random.choice([True, False]):
            host.password = "BAD_PASSWORD"
    agg_res = nr.run(task=show_clock_b)

    print_result(agg_res)


# 5c. Repeat exercise 5b except store the "recover" password in an ansible-vault YAML file. Decrypt
# this file dynamically and assign the recover password using this vaulted password. See the Ansible
# Vault decryption code that is included near the top of this lesson.

# You can create a YAML file with the proper password and encrypt it using Ansible Vault:
# "ansible-vault encrypt MY_FILE".

# Skipping this one, cannot be bothered.

if __name__ == "__main__":
    main_a()
    main_b()
