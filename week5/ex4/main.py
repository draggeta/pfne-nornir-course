#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result, MultiResult
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_string, template_file

# 4a. In a new script, create a Jinja2 representation of the ACL from the previous task; this Jinja2
# template should just be an embedded string in your script. Using the same external YAML/JSON file
# for source data, construct the ACL from the previous task, render it, and print this ACL out to
# standard output. Your output should be identical to the output of exercise3.

# 4b. Create an "acl.j2" file that is the Jinja2 representation of the ACL from the previous task.
# Recreate your script from exercise4a except use the external Jinja2 file for the template. Your
# output should once again be the fully generated ACL.

# 4c. Add a step to your custom task to render the ACL and store the rendered value as an attribute
# of the "srx2" host (in other words, store the ACL data in the Nornir host object). Once again
# print the fully rendered ACL to standard out (this time using the host object attribute where you
# stored the ACL data).

ACL_TEMPLATE = """
{%- for acl, acl_list in acls.items() %}
    {%- for ace in acl_list %}
set firewall family inet filter {{ acl }} term {{ ace['term_name'] }} from protocol {{ ace['protocol'] }}
set firewall family inet filter {{ acl }} term {{ ace['term_name'] }} from destination-port {{ ace['destination_port'] }}
set firewall family inet filter {{ acl }} term {{ ace['term_name'] }} from destination-address {{ ace['destination_address'] }}
set firewall family inet filter {{ acl }} term {{ ace['term_name'] }} then {{ ace['state'] }}
    {%- endfor %}
{% endfor %}
"""


def gen_acl_inline(task):
    acl_data = task.run(task=load_yaml, file="acl.yaml")
    acl_list = acl_data[0].result

    multi_res = task.run(task=template_string, template=ACL_TEMPLATE, acls=acl_list)

    print_result(multi_res)


def gen_acl_template(task):
    acl_data = task.run(task=load_yaml, file="acl.yaml")
    acl_list = acl_data[0].result

    multi_res = task.run(task=template_file, template="acl.j2", path=".", acls=acl_list)

    print_result(multi_res)


def gen_acl_add_var(task):
    acl_data = task.run(task=load_yaml, file="acl.yaml")
    acl_list = acl_data[0].result

    multi_res = task.run(
        task=template_file, template="acl.j2", path=".", acls=acl_list, name="boooo"
    )
    task.host["acls"] = multi_res[0].result

    test = MultiResult(name="heuh")
    test.append(
        Result(host=task.host, result=task.host["acls"], failed=False, changed=False)
    )
    print_result(test)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(name="srx2"))

    nr.run(gen_acl_inline)
    nr.run(gen_acl_template)
    nr.run(gen_acl_add_var)


if __name__ == "__main__":
    main()
