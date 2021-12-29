#!/usr/bin/env python

import os

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.inventory import ConnectionOptions

# from nornir.core.inventory import ConnectionOptions
from nornir_netmiko.tasks.netmiko_send_command import netmiko_send_command
from nornir_utils.plugins.functions.print_result import print_result

# 4a. Setup the Cisco NX-OS devices to use a Netmiko session log. Use a single session log defined
# in groups.yaml for both NX-OS devices. Set runner plugin to "serial" so that threading doesn't
# cause issues with the session_log.

# Create a Nornir script that uses the "netmiko_send_command" task-plugin and executes on only these
# two NX-OS devices. Monitor the output of the session log file and see what is occurring in the
# Netmiko session. For this exercise and for exercise 4b, set the password using an environment
# variable (instead of using a password embedded in inventory). Once again, you can use
# "tail -f filename" to tail the session_log file to see what is happening real-time.


def main_a():
    nr = InitNornir(config_file="config.yaml", runner={"plugin": "serial"})
    nr = nr.filter(F(platform="nxos"))

    for _, host in nr.inventory.hosts.items():
        host.password = PASSWD

    agg_res = nr.run(
        task=netmiko_send_command, command_string="show ip interface brief"
    )
    print_result(agg_res)


# 4b. Expand on exercise4a to create a per-device session log for the two NX-OS devices (use the
# Nornir device "name" as part of the session_log file name). Set the session_log name dynamically
# in a custom task.


def show_ip_b(task):
    s_log = f"{task.host}_session.log"

    task.host.groups[0].connection_options["netmiko"].extras["session_log"] = s_log
    task.run(task=netmiko_send_command, command_string="show ip interface brief")


def main_b():
    nr = InitNornir(config_file="config.yaml", runner={"plugin": "serial"})
    nr = nr.filter(F(platform="nxos"))

    for _, host in nr.inventory.hosts.items():
        host.password = PASSWD

    agg_res = nr.run(task=show_ip_b)
    print_result(agg_res)


PASSWD = os.getenv("NORNIR_PASSWORD", "None")

if __name__ == "__main__":
    main_a()
    main_b()
