#!/usr/bin/env python

# 4a. Write a script with a custom task that uses "napalm_configure" to deploy the same VLAN
# configuration as exercise 3.

# import napalm modules to avoid current locking issue with imports in NAPALM
import napalm.eos  # noqa
import napalm.nxos  # noqa

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure


def configure_vlan(task, vlan_id, vlan_name):
    config_string = f"""vlan {vlan_id}
  name {vlan_name}"""
    task.run(task=napalm_configure, configuration=config_string)


def main():

    VLAN_ID = "123"
    VLAN_NAME = "ntp_vlan"

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(task=configure_vlan, vlan_id=VLAN_ID, vlan_name=VLAN_NAME)
    print_result(result)


if __name__ == "__main__":
    main()
