#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.configuration import T
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command

# Create a Nornir object
nr = InitNornir(config_file="config.yaml")

# 2a. Filter your inventory to select ONLY devices that belong to the "ios"
# group.

filt = F(groups__contains="ios")
nr = nr.filter(filt)

print(nr.inventory.hosts)

# 2b. Create a Python script that uses netmiko_send_command to execute
# "show run | inc hostname" on all the "ios" devices in your inventory (once
# again use the filter that you created in exercise 2a).
# Assign the result of this task to a variable named "my_results".
#
# Print the "type" of the my_results object.
# Additionally, inspect the my_results object using its "keys()", "items()" and
# "values" methods.

my_results = nr.run(
    # name="Get hostname from running config",
    task=netmiko_send_command,
    command_string="show run | inc hostname",
)

print(f"my_results type: {type(my_results)}")
print(f"my_results keys(): {my_results.keys()}")
print(f"my_results items(): {my_results.items()}")
print(f"my_results values(): {my_results.values()}")
print()

# 2c. Assign the results from "cisco3" to a new variable named "host_results".
# Inspect this new MultiResult object: access the zeroith element from this
# MultiResult object. Finally, determine if "host_results" is an iterable or
# not.

host_results = my_results["cisco3"]
print(f"host_results type: {type(host_results)}")
print(f"host_results element 0: {repr(host_results[0])}")
print(f"host_results iterable: {host_results.__iter__}")
print()

# 2d. Assign the zeroith element of the host_results object to a new variable
# named "task_result". What type of object is task_result? Print out the
# 'host', 'name', 'result', and 'failed' attributes from task_result. Which
# field actually contains the output from the network device?

task_result = host_results[0]

print(f"task_result type: {type(task_result)}")
print(f"task_result host: {task_result.host}")
print(f"task_result name: {task_result.name}")
print(f"task_result result: {task_result.result}")  # contains the output
print(f"task_result failed: {task_result.failed}\n")
print()

# 2e. Looking back at exercises 2a - 2d: explain what Nornir result types are
# "my_results", "host_results", and "task_result"? What purpose does each of
# those three data types serve (i.e. why do we have them)?

# my_results is of type AggregatedResult and contains all results across all
# devices.
# host_results is of the type MultiResult and contains all results for the host
# (all tasks that have run on the host).
# task_result is of the type Result and contains the result of a task that
# has been executed on a host.
