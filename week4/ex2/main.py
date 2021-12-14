#!/usr/bin/env python

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_file_transfer, netmiko_send_command
from nornir_utils.plugins.functions import print_result

# 2a. Create a new directory named "eos". In this "eos" directory create a file named
# "arista_test.txt". In this "arista_test.txt" file add some unique content that you will be able to
# identify. This unique content will let verify that your particular file was transferred to the
# remote device.

# Next, copy the hosts.yaml, groups.yaml, and defaults.yaml files from ~/nornir_inventory to your
# current directory. Modify the groups.yaml file and add the following to the "eos" group:

#   data:
#     file_name: arista_test.txt

# Now, using the "netmiko_file_transfer" task-plugin, secure copy your arista_test.txt file to all
# of the Arista switches in the lab environment.

# Please use the "platform" attribute from inventory to specify the directory name. Additionally,
# please use the "file_name" variable from inventory. In other words, construct
# "eos/arista_test.txt" entirely from inventory information.

# Note, you will want to pass the following argument into the "netmiko_file_transfer" task-plugin:

#     overwrite_file=True,

# This will allow the "netmiko_file_transfer" task-plugin to overwrite the file if it already
# exists.


def gen_file_transfer2a(task):
    platform = task.host.platform
    file_name = task.host["file_name"]
    task.run(
        task=netmiko_file_transfer,
        overwrite_file=True,
        source_file=f"{platform}/{file_name}",
        dest_file=file_name,
        direction="put",
    )


def main2a():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(platform="eos")

    res = nr.run(task=gen_file_transfer2a)
    print_result(res)


# 2b. Repeat exercise2a except now create a custom task that performs both a file transfer and a
# verify operation. The custom_task should execute the "netmiko_file_transfer" task-plugin (as
# before) and should also execute the following command (using the "netmiko_send_command"
# task-plugin):

#     more flash:/arista_test.txt

# Your program should print the contents of the remote file to the screen.


def gen_file_transfer2b(task):
    platform = task.host.platform
    file_name = task.host["file_name"]
    task.run(
        task=netmiko_file_transfer,
        overwrite_file=True,
        source_file=f"{platform}/{file_name}",
        dest_file=file_name,
        direction="put",
    )

    task.run(task=netmiko_send_command, command_string=f"more flash:/{file_name}")


def main2b():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(platform="eos")

    res = nr.run(task=gen_file_transfer2b)
    print_result(res)


# 2c. Create a Nornir script that copies "arista_test.txt" from each of the remote Arista devices
# (secure copy, "get" operation) and saves the file as "eos/{device_name}-saved.txt" where
# {device_name} is the Nornir device name.


def gen_file_transfer2c(task):
    host = task.host.name
    platform = task.host.platform
    file_name = task.host["file_name"]
    task.run(
        task=netmiko_file_transfer,
        overwrite_file=True,
        source_file=f"{file_name}",
        dest_file=f"{platform}/{host}-saved.txt",
        direction="get",
    )


def main2c():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(platform="eos")

    res = nr.run(task=gen_file_transfer2c)
    print_result(res)


if __name__ == "__main__":
    main2a()
    main2b()
    main2c()
