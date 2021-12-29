#!/usr/bin/env python

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_napalm.plugins.tasks import napalm_configure

# 5a. Write a script that captures the running configuration from "arista4" using the NAPALM
# "config" getter. Print this configuration out to the screen.


def main_a():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")
    agg_result = nr.run(task=napalm_get, getters=["config"], retrieve="running")
    arista4_result = agg_result["arista4"][0].result
    arista4_running_config = arista4_result["config"]["running"]

    file_name = "arista4-running.txt"
    with open(file_name, "w") as f:
        f.write(arista4_running_config)
    print()
    print("#" * 40)
    print(arista4_running_config)
    print("#" * 40)
    print()


# 5b. Use napalm_configure to add a new loopback interface to the "arista4" device. Your
# configuration should be similar to the following:

# interface Loopback123
#    description Hello


def main_b():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")

    # Current running config
    agg_result = nr.run(task=napalm_get, getters=["config"], retrieve="running")
    arista4_result = agg_result["arista4"][0].result
    arista4_running_config = arista4_result["config"]["running"]  # noqa

    # New config
    config = """
interface loopback123
  description verycoolloopback
    """
    agg_result = nr.run(task=napalm_configure, configuration=config)
    print_result(agg_result)


# 5c. Create a new program that combines both exercise5a and exercise5b. First, retrieve the current
# running configuration from Arista4, then configure the loopback interface. Finally, use "
# napalm_configure" and the full configuration replace operation to restore the previously captured
# running configuration. The net effect of this last step should be to remove the loopback
# configuration (i.e. to restore the running configuration to its original state).


def main_c():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")

    # Capture current running configuration
    agg_result = nr.run(task=napalm_get, getters=["config"], retrieve="running")
    arista4_result = agg_result["arista4"][0].result
    arista4_running_config = arista4_result["config"]["running"]

    # Configure a new loopback
    config = """interface loopback123
  description verycoolloopback"""
    agg_result = nr.run(task=napalm_configure, configuration=config)
    print_result(agg_result)

    print()

    # Completely resture the configuration using configure replace
    agg_result = nr.run(
        task=napalm_configure, configuration=arista4_running_config, replace=True
    )
    print_result(agg_result)


if __name__ == "__main__":
    main_a()
    main_b()
    main_c()
