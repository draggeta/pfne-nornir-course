#!/usr/bin/env python

from getpass import getpass
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks.netmiko_send_command import netmiko_send_command
from nornir_utils.plugins.functions.print_result import print_result

# 3a. Configure logging level specified in config.yaml to DEBUG; also change the logging output file
# name in config.yaml. Create a Nornir script that executes a netmiko_send_command operation. Watch
# the log file as the script executes (tail -f filename). For this exercise and exercise 3b, set the
# credentials for the Nornir devices using getpass() (instead of using a password embedded in
# inventory).


def main_a():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="eos"))

    for _, host in nr.inventory.hosts.items():
        host.password = PASSWD

    agg_res = nr.run(task=netmiko_send_command, command_string="show interface")

    print_result(agg_res)


# 3b. Add a logger configuration into your Nornir script and send a few log messages at the "debug",
# "error", and "critical" levels. Confirm your messages make it into your log file.

import logging


def main_b():
    LOGGER.info("Starting tasks.")
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="eos"))
    for _, host in nr.inventory.hosts.items():
        host.password = PASSWD
    nr.run(task=netmiko_send_command, command_string="show mac address-table")
    LOGGER.error("Some error")
    LOGGER.debug("Tasks finished.")


if __name__ == "__main__":
    LOGGER = logging.getLogger("nornir")
    LOGGER.critical("Setting the password.")
    PASSWD = getpass()
    main_a()
    main_b()
