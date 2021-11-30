#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# Create a Nornir object
nr = InitNornir(config_file="config.yaml")

# 5a. Create a Nornir script that uses the netmiko_send_command task-plugin to
# execute "show ip int brief" on each of the devices in the "ios" group. Use
# the inventory filtering pattern that we used in earlier exercises. Print the
# output from this task using the print_results function.

filt = F(groups__contains="ios")
nr = nr.filter(filt)

nm_results = nr.run(task=netmiko_send_command, command_string="show ip int brief")

print_result(nm_results)


# 5b. Expanding on exercise 5a, set the 'cisco3' password attribute to an
# invalid value. The code to do this would be similar to the following:

# nr.inventory.hosts["cisco3"].password = 'bogus'

nr = InitNornir(config_file="config.yaml")
filt = F(groups__contains="ios")
nr = nr.filter(filt)

nr.inventory.hosts["cisco3"].password = "bogus"

# Re-run your Nornir task and print out the "failed_hosts" using both the
# results object (results.failed_hosts) and the Nornir object
# (nr.data.failed_hosts)

nm_results = nr.run(task=netmiko_send_command, command_string="show ip int brief")

print(
    f"task failed: {nm_results.failed_hosts}"
    f"Global failed hosts: {nr.data.failed_hosts}"
)

# 5c. Expand upon the Python program in exercise5b, this time add an additional
#  task that runs *only* on the failed hosts.

# In other words, the sequence of actions should be:
# i.   Filter your hosts to only be the "ios" hosts.
# ii.  Set the "password" for "cisco3" to be an invalid password.
# iii. Execute "show ip int brief" on all of the "ios" hosts ("cisco3" will
#      fail due to the invalid password).
# iv.  Set the "cisco3" password back to its correct value using
#      os.environ["NORNIR_PASSWORD"] (this environment variable will be set in
#      the lab environment).
# v.   Execute "show ip int brief" again, but this time execute the task only
#      on the "failed_hosts" (i.e. cisco3). This will require that you set the
#      "on_good" and "on_failed" arguments that are used in the Nornir .run()
#      method.

# Re-set password back to valid value
nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]

# Re-run only on failed hosts
print()
my_results = nr.run(
    task=netmiko_send_command,
    command_string="show ip int brief",
    on_good=False,
    on_failed=True,
)
print_result(my_results)
print()
print(f"Task failed hosts: {my_results.failed_hosts}")
print(f"Global failed hosts: {nr.data.failed_hosts}")
print()

# 5d. Expand on exercise 5c except at the very end of your program, recover the
# failed host. Print out the global failed hosts before and after you do this.
# At this point there should be no failed hosts.

# Re-run only on failed hosts
    my_results = nr.run(
        task=netmiko_send_command,
        command_string="show ip int brief",
        on_good=False,
        on_failed=True,
    )

    print("\n\n")
    print("Executing Task: only on cisco3 - task should succeed:")
    print("-" * 40)
    print_result(my_results)
    print()
    print(f"Task failed hosts: {my_results.failed_hosts}")
    print(f"Global failed hosts: {nr.data.failed_hosts}")
    print("\n\n")
    print("Recovering failed_host")
    print("-" * 40)
    nr.data.recover_host("cisco3")
    print(f"Global failed hosts: {nr.data.failed_hosts}")
    print()
