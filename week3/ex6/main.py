#!/usr/bin/env python

import urllib3

from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from pprint import pprint

# Disable the SSL cert warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 6a. Using the config.yaml file from exercise 4, create a new Nornir object that filters to only
# the "nxos" devices. Using the "napalm_get" task-plugin, retrieve the configuration from these
# devices. Print the results of this task.

print("6A" * 45)
print("6A" * 45)
nr = InitNornir(config_file="config.yaml")
nxd = nr.filter(F(groups__contains="nxos"))
print_result(nxd.run(task=napalm_get, getters=["config"]))

# # 6b. Filter the napalm "get" to capture only the running configuration. Print the results of the
# # task.

# print("6B" * 45)
# print("6B" * 45)
# gopt = {"config": {"retrieve": "running"}}
# print_result(nxd.run(task=napalm_get, getters=["config"], getters_options=gopt))

# # 6c. Modify the script to get the running configuration AND facts from the device. Once again,
# # print the results.

# print("6C" * 45)
# print("6C" * 45)
# gopt = {"config": {"retrieve": "running"}}
# print_result(
#     nxd.run(task=napalm_get, getters=["config", "facts"], getters_options=gopt)
# )

# 6d. Finally, modify the code to capture all configurations (continue to use the
# "getters_options"), and the facts. For each device, parse the data and indicate whether the
# startup and running configs match and print out this information along with some of the basic
# device information. Your output should be similar to the following:

# {'nxos1': {'model': 'Nexus9000 9000v Chassis',
#            'start_running_match': True,
#            'uptime': 7172937,
#            'vendor': 'Cisco'},
#  'nxos2': {'model': 'Nexus9000 9000v Chassis',
#            'start_running_match': True,
#            'uptime': 7172474,
#            'vendor': 'Cisco'}}

# *Note* startup and running config contain timestamps--remove those timestamps before comparing the
# configurations!

print("6D" * 45)
print("6D" * 45)
gopt = {"config": {"retrieve": "all"}}
res = nxd.run(task=napalm_get, getters=["config", "facts"], getters_options=gopt)

output = {}
for _, v in res.items():
    conf_startup = v[0].result["config"]["startup"]
    conf_running = v[0].result["config"]["running"]

    s_startup = conf_startup.find("version")
    s_running = conf_running.find("version")

    conf_startup = conf_startup[s_startup:]
    conf_running = conf_running[s_running:]

    conf_match = conf_startup == conf_running

    facts = v[0].result["facts"]
    output[facts["hostname"]] = {
        "model": facts["model"],
        "start_running_match": conf_match,
        "vendor": facts["vendor"],
        "uptime": facts["uptime"],
    }

pprint(output)
