#!/usr/bin/env python

from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.functions import print_result

# 3a. Create a JSON or a YAML file that contains the required data to construct three ACL entries
# for Juniper. It should be similar to the following (in terms of the data structure and required
# fields):

# ---
# my_acl:
#   - protocol: tcp
#     destination_port: 22
#     destination_address: 1.2.3.4/32
#     term_name: rule1
#     state: accept
#   - protocol: tcp
#     destination_port: 443
#     destination_address: 1.2.3.4/32
#     term_name: rule2
#     state: accept
#   - protocol: tcp
#     destination_port: 443
#     destination_address: 1.2.3.4/32
#     term_name: rule3
#     state: discard


# 3b. Filter the Nornir inventory to just the srx2 device. Write a custom task to generate the
# firewall rules for each entry in the YAML/JSON file. Print the generated rules to your standard
# output. Your output should look as follows:

# set firewall family inet filter my_acl term rule1 from protocol tcp
# set firewall family inet filter my_acl term rule1 from destination-port 22
# set firewall family inet filter my_acl term rule1 from destination-address 1.2.3.4/32
# set firewall family inet filter my_acl term rule1 then accept
# set firewall family inet filter my_acl term rule2 from protocol tcp
# set firewall family inet filter my_acl term rule2 from destination-port 443
# set firewall family inet filter my_acl term rule2 from destination-address 1.2.3.4/32
# set firewall family inet filter my_acl term rule2 then accept
# set firewall family inet filter my_acl term rule3 from protocol tcp
# set firewall family inet filter my_acl term rule3 from destination-port 443
# set firewall family inet filter my_acl term rule3 from destination-address 1.2.3.4/32
# set firewall family inet filter my_acl term rule3 then discard

# You do not need to push these configuration changes out to the SRX.


def gen_acl(task):
    acl_data = task.run(task=load_yaml, file="acl.yaml")
    for k, v in acl_data[0].result.items():
        for acl in v:
            print(
                f"set firewall family inet filter {k} term {acl['term_name']} from protocol {acl['protocol']}\n"
                f"set firewall family inet filter {k} term {acl['term_name']} from destination-port {acl['destination_port']}\n"
                f"set firewall family inet filter {k} term {acl['term_name']} from destination-address {acl['destination_address']}\n"
                f"set firewall family inet filter {k} term {acl['term_name']} then {acl['state']}\n"
            )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")

    res = nr.run(task=gen_acl)
    print_result(res)


if __name__ == "__main__":
    main()
