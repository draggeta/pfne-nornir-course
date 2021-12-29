#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

from nornir_netmiko.tasks import netmiko_send_command


# 1a. Create a Nornir script that will send an invalid command to the Junos "srx2" device (for
# example, "show ip interface" does not work on Junos).

# Netmiko will not attempt to interpret the output of this invalid command.

# Use the "print_result" function to ensure that the task succeeded and to inspect the output
# received back from the device. Note, the "syntax error" message is from the Junos SRX and is not a
# Python exception.


def show_ip_int_a(task):
    task.run(task=netmiko_send_command, command_string=f"show ip interface")


def main_a():
    nr = InitNornir(config_file="config.yaml")

    nr = nr.filter(F(name="srx2"))

    res = nr.run(task=show_ip_int_a)

    print_result(res)


# 1b. Modify your custom task to raise a ValueError exception if "syntax error" is detected in the
# Netmiko send_command output. This exception raising should be inside the custom task.


def show_ip_int_b(task):
    res = task.run(task=netmiko_send_command, command_string=f"show ip interface")

    if "syntax error" in res[0].result:
        raise ValueError


def main_b():
    nr = InitNornir(config_file="config.yaml")

    nr = nr.filter(F(name="srx2"))

    res = nr.run(task=show_ip_int_b)

    print_result(res)


if __name__ == "__main__":
    main_a()
    main_b()
