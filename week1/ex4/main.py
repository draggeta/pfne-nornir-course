#!/usr/bin/env python

from nornir import InitNornir

# Create a Nornir object
nr = InitNornir()


def print_host(task):
    print(f"Running on host '{task.host}'")
    print(f"Hostname is '{task.host.hostname}'\n")


nr.run(task=print_host)
