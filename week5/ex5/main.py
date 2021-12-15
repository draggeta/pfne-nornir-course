#!/usr/bin/env python

from time import sleep

import urllib3

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import MultiResult, AggregatedResult
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file

from nornir_utils.plugins.functions import print_result

from nornir_napalm.plugins.tasks import napalm_configure, napalm_get

# Disable the SSL cert warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 5a. Create a new directory named "nxos". In this directory, create a Jinja2 BGP template for the
# NX-OS platform. This template should contain variables for AS Number, BGP router-ID, and a basic
# peering setup. Your BGP template should look similar to the following:

# router bgp {{ bgp_asn }}
#   router-id {{ bgp_router_id }}
#   neighbor {{ bgp_peer }}
#     remote-as {{ bgp_remote_asn }}
#     address-family ipv4 unicast

# Additionally, create a simple interface template with variables for interface name, IP address,
# and subnet mask. Your interface template should look similar to the following:

# interface {{ int_name }}
#  no switchport
#  ip address {{ ip_address }} {{ ip_mask }}
#  no shutdown


# 5b. Copy the "hosts.yaml" file from ~/nornir_inventory into your working directory. Create a
# config.yaml file that uses this new "hosts.yaml" file. Both the "groups.yaml" and the
# "defaults.yaml" files should continue to be the standard ~/nornir_inventory files. In your new
# hosts.yaml file add all the necessary variables to render the two Jinja2 templates. These
# variables should all be added into the "data" attribute for nxos1 and nxos2.

# Additional details on the required variables:

# * "bgp_asn" use a value of 22
# * "int_name" select a random interface from Ethernet1/1 through Ethernet1/4 (choose the same
#       interface for both nxos1 and nxos2)

# For IP addressing use something from RFC1918 such as a random /24 from the 172.20.0.0/16 range

# Note, the end goal is to have a working BGP peering session between nxos1 and nxos2. Consequently,
# you need to choose the same Ethernet interface for both nxos1 and nxos2. You also need to choose
# the same IP subnet for nxos1 and nxos2. Finally your BGP peering information needs to match your
# IP address information.

# Create another new directory named "rendered_configs" and write these rendered configuration to
# disk (four total rendered files: a BGP file and an interface file for each nxos host). Validate
# that the configurations look correct.


def gen_config(task):
    path = f"./{task.host.platform}"
    bgp_conf = task.run(task=template_file, template="bgp.j2", path=path, **task.host)
    int_conf = task.run(
        task=template_file, template="interfaces.j2", path=path, **task.host
    )
    # with open(file=f"./rendered_configs/{task.host.name}-bgp.conf", mode="w") as f:
    #     f.write(bgp_conf[0].result)
    # with open(file=f"./rendered_configs/{task.host.name}-int.conf", mode="w") as f:
    #     f.write(int_conf[0].result)
    bgpt = task.run(
        task=write_file,
        filename=f"./rendered_configs/{task.host.name}-bgp.conf",
        content=bgp_conf[0].result,
    )
    intt = task.run(
        task=write_file,
        filename=f"./rendered_configs/{task.host.name}-int.conf",
        content=int_conf[0].result,
    )

    # return bgpt, intt


# 5c. Using NAPALM configure, read the stored configurations from the rendered_configs directory and
# deploy the configurations to the nxos hosts. Use a NAPALM merge operation for this task.

# Use the NAPALM "bgp_neighbors" getter to verify that your BGP peering session becomes established.
# Note, you might need to add a time.sleep delay between the configuration step and the verification
# step (in other words allow the BGP session sufficient time to reach the established state).


def psh_config(task):
    path = "./rendered_configs"
    host = task.host.name

    # with open(f"{path}/{host}-bgp.conf", "r") as f:
    #     bgp_conf = "\n".join(f.readlines)
    # with open(f"{path}/{host}-int.conf", "r") as f:
    #     int_conf = "\n".join(f.readlines)

    task.run(task=napalm_configure, filename=f"{path}/{host}-int.conf", dry_run=False)
    task.run(task=napalm_configure, filename=f"{path}/{host}-bgp.conf", dry_run=False)

    sleep(10)

    task.run(task=napalm_get, getters=["bgp_neighbors"])

    # return intc, bgpc, check


def config(task):
    task.run(task=gen_config)
    task.run(task=psh_config)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="nxos"))

    res = nr.run(task=config)

    print_result(res)


if __name__ == "__main__":
    main()
