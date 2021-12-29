#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result

from nornir_jinja2.plugins.tasks import template_file


# 2a. Create a Jinja2 template that generates loopback interfaces for NX-OS devices. Your Jinja2
# template should look similar to the following:

# {% for inf in loopbacks %}
# loopback {{ inf.id }}
#   description inf.description
#   ip address {{ inf.ip }} {{ inf.mask }}
# {% endfor %}

# This template should use a data structure defined in inventory similar to the following:

# data:
#   loopbacks:
#     - id: 123
#       description: ntp source
#       ip: 1.2.3.1
#       mask: 255.255.255.255

# Note, the value "loopbacks" is a list that contains an inner dictionary (with fields of "id",
# "description", "ip", "mask").

# Copy the ~/nornir_inventory/hosts.yaml file to your working directory and add a "loopbacks" key
# inside data for each of the NX-OS hosts (similar to what is specified above).

# In your Nornir script, filter your inventory to just the "nxos" hosts. Create a custom task that
# uses the inventory data and the Jinja2 template to render the configuration. Use the print_result
# function to ensure that your template renders correctly for each NX-OS device.


def render_template_a(task):
    path = f"./{task.host.platform}"
    task.run(task=template_file, template="loopback.j2", path=path, **task.host)


def main_a():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="nxos"))

    agg_res = nr.run(task=render_template_a)

    print_result(agg_res)


# 2b. In Nornir inventory, comment out or otherwise remove the "data > loopbacks" section for
# "nxos2". Re-execute your Nornir script--at this point, there should be a failure (i.e. certain
# Jinja2 variables are not known).

# Modify your custom task such that the exception returned from Jinja2 "template_file" call is
# gracefully handled in the subtask (using NornirSubTaskError).


def render_template_b(task):
    path = f"./{task.host.platform}"
    try:
        task.run(task=template_file, template="loopback.j2", path=path, **task.host)
    except NornirSubTaskError:
        return "Template error occurred."


def main_b():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="nxos"))

    agg_res = nr.run(task=render_template_b)

    print_result(agg_res)


# 2c. [Optional] - Further modify your custom task such that the multi_result execution reports
# "failed" as False. In other words, exercise 2b gracefully caught the exception in the subtask,
# but Nornir multi_result will still report the multi_result as failed:

# ipdb> multi_result = agg_result["nxos2"]
# ipdb> multi_result.failed
# True
# ipdb> multi_result[0].failed
# False
# ipdb> multi_result[1].failed
# True

# Nornir performs an "any" operation on the multi_result to determine "failed" so if any of the
# subtasks failed, then the overall multi_result will still be reported as "failed". So even though
# we gracefully caught the exception, the exception/failure of the template rendering still happened
# and is still reflected in the multi_result:

# ipdb> multi_result[1].exception
# UndefinedError("'loopbacks' is undefined",)
# ipdb> multi_result[1].failed
# True

# The above is from the Jinja2 templating task in the multi_result.


# But you can remove "results" from inside the subtask using.

#    except NornirSubTaskError:
#        task.results.pop()

# And then you can return your own custom Result object.

#    msg = "Encountered Jinja2 error"
#    return Result(
#        changed=False,
#        diff=None,
#        result=msg,
#        host=task.host,
#        failed=False,
#        exception=None,
#    )

# The end result should be that back in your "main" program that there is "no failure". In other
# words, this is potentially showing you how you could hide failures that you don't care about.

# ipdb> p agg_result["nxos2"]
# MultiResult: [Result: "render_configurations"]
# ipdb> p agg_result["nxos2"].failed
# False


def render_template_c(task):
    path = f"./{task.host.platform}"
    try:
        task.run(task=template_file, template="loopback.j2", path=path, **task.host)
    except NornirSubTaskError:
        task.results.pop()
        msg = "Encountered Jinja2 error"
        return Result(
            changed=False,
            diff=None,
            result=msg,
            host=task.host,
            failed=False,
            exception=None,
        )


def main_c():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(platform="nxos"))

    agg_res = nr.run(task=render_template_c)

    print_result(agg_res)


if __name__ == "__main__":
    # main_a()
    main_b()
    main_c()
