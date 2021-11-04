#!/usr/bin/env python

from nornir import InitNornir

# Create a Nornir object
nr = InitNornir()


def print_host(task):
    print(f"Running on host '{task.host}'")
    print(f"Hostname is '{task.host.hostname}'")
    print(f"DNS 1: '{task.host['dns1']}'")
    print(f"DNS 2: '{task.host['dns2']}'\n")


nr.run(task=print_host)
