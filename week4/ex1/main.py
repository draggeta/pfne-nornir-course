#!/usr/bin/env python

import re

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# 1a. Create a custom task that uses the 'netmiko_send_command' task-plugin to query all of the lab
# devices for their uptime. This task will require that you execute different commands based on the
# platform (see the table below):

# Platform                    Command
# --------                    -----------
# Cisco IOS/NX-OS             show version | inc uptime
# Arista                      show version | inc Uptime
# Juniper SRX                 show system uptime | match System

# Print out the Nornir device name and the uptime string for each of the hosts.


def gen_uptime(task):
    cmd = {
        "ios": "show version | inc uptime",
        "nxos": "show version | inc uptime",
        "eos": "show version | inc Uptime",
        "junos": "show system uptime | match System",
    }

    plat = task.host.platform
    command = cmd[plat]

    task.run(task=netmiko_send_command, command_string=command)


def main1a():
    nr = InitNornir(config_file="config.yaml")

    agg_results = nr.run(task=gen_uptime)

    for host, results in agg_results.items():
        print(f"{host:7}: {results[1].result.strip()}")


# 1b. Process the returned uptime string and convert it over to uptime seconds. If the uptime is
# less than 1 day, then print out a notice that the device recently rebooted.

# Note, you can skip the uptime string conversion for the Juniper device and just have it return a
# value of 90 seconds for the "uptime seconds" (in other words, artificially pretend that the
# Juniper device just rebooted).

# For reference, you can re-use the function referenced here to assist you with this exercise. You
# will need to make modifications to this function, however (technically in NAPALM "parse_uptime" is
# a static method, but we recommend that you copy this and convert it to a normal function in your
# program):

# https://github.com/napalm-automation/napalm/blob/2.4.0/napalm/ios/ios.py#L894

HOUR_SECONDS = 3600
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS
YEAR_SECONDS = 365 * DAY_SECONDS


def parse_uptime(uptime_str):
    """
    Extract the uptime string from the given Cisco IOS Device.
    Return the uptime in seconds as an integer
    """
    # Initialize to zero
    (years, weeks, days, hours, minutes) = (0, 0, 0, 0, 0)

    uptime_str = uptime_str.strip()
    time_list = uptime_str.split(",")
    for element in time_list:
        if re.search("year", element):
            years = int(element.split()[0])
        elif re.search(r"Uptime: \d+ week", element):
            weeks = int(element.split()[1])
        elif re.search("week", element):
            weeks = int(element.split()[0])
        elif re.search(r"Kernel uptime is \d+ day", element):
            days = int(element.split()[3])
        elif re.search("day", element):
            days = int(element.split()[0])
        elif re.search("\d+ hours and \d+ minutes", element):
            hours = int(element.split()[0])
            minutes = int(element.split()[3])
        elif re.search("hour", element):
            hours = int(element.split()[0])
        elif re.search(r"uptime is \d+ minutes", element):
            minutes = int(element.split()[3])
        elif re.search("minute", element):
            minutes = int(element.split()[0])
        elif re.search(r"\(\d+:\d+:\d+ ago\)", element):
            hours = int(element.split("(")[1].split()[0].split(":")[0])
            minutes = int(element.split("(")[1].split()[0].split(":")[1])

    uptime_sec = (
        (years * YEAR_SECONDS)
        + (weeks * WEEK_SECONDS)
        + (days * DAY_SECONDS)
        + (hours * 3600)
        + (minutes * 60)
    )
    return uptime_sec


def gen_uptime(task):
    cmd = {
        "ios": "show version | inc uptime",
        "nxos": "show version | inc uptime",
        "eos": "show version | inc Uptime",
        "junos": "show system uptime | match System",
    }

    plat = task.host.platform
    command = cmd[plat]

    task.run(task=netmiko_send_command, command_string=command)


def main1b():
    nr = InitNornir(config_file="config.yaml")

    agg_results = nr.run(task=gen_uptime)

    for host, results in agg_results.items():
        upsec = parse_uptime(results[1].result.strip())
        if upsec > DAY_SECONDS:
            print(f"{host:7}: {upsec}")
        else:
            print(f"{host:7}: {upsec}, recently (re)booted")


if __name__ == "__main__":
    # main1a()
    main1b()
