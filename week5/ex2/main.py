#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

# 2a. Copy the "defaults.yaml" file from ~/nornir_inventory into your working directory. Create a
# config.yaml file to use this new "defaults.yaml" file as well as the hosts.yaml and groups.yaml
# files from exercise1. Using defaults.yaml, set a default port of "22" for all of your hosts.

# 2b. Create a Python script. In this script, initialize Nornir and filter the inventory to just the
# eos" devices. Next use the "napalm_get" task-plugin and use the "config" getter to retrieve the
# configuration of the eos devices. Execute the script--at this point the script should fail as the
# eAPI port is not port 22!


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="eos"))
    res = nr.run(task=napalm_get, getters=["config"])

    print_result(res)


# 2c. Modify your "groups.yaml" file such that your script succeeds.

if __name__ == "__main__":
    main()
