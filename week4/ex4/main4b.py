#!/usr/bin/env python

# 4b. Modify your custom task to add a keyword argument for the "dry_run" setting. Set this argument
# to False by default. In the main part of your program call this custom task and test both
# dry_run=True and dry_run=False. Note, for napalm_configure and dry_run=True, NAPALM will not
# actually make any configuration changes--instead NAPALM and Nornir will report whether any changes
# would have been made.

# import napalm modules to avoid current locking issue with imports in NAPALM
import napalm.eos  # noqa
import napalm.nxos  # noqa

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

from nornir_napalm.plugins.tasks import napalm_configure


def configure_vlan(task, vlan_id, vlan_name, dry_run=True):
    config_string = f"""vlan {vlan_id}
  name {vlan_name}"""
    task.run(task=napalm_configure, configuration=config_string, dry_run=dry_run)


def main():

    VLAN_ID = "123"
    VLAN_NAME = "ntp_vlan"
    DRY_RUN = False

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(
        task=configure_vlan, vlan_id=VLAN_ID, vlan_name=VLAN_NAME, dry_run=DRY_RUN
    )
    print_result(result)


if __name__ == "__main__":
    main()
