#!/usr/bin/env python

import os

from nornir import InitNornir


# Create a Nornir object
nr = InitNornir()

# 1a. Now create a Python script that uses InitNornir to initialize a Nornir
# object. Using this Nornir object print out the number of workers currently
# configured. This value should be 20 at this point.
print(f"Worker default count: {nr.runner.num_workers}")

# 1b. Create a Nornir config.yaml file that sets the number of workers to 5.
# Modify the Python script from exercise 1a to load this config.yaml file.
# Print out and verify the new number of workers.

nr = InitNornir(config_file="config_runner.yaml")
print(f"Worker config count : {nr.runner.num_workers}")

# 1c. Use:
# export NORNIR_RUNNER_OPTIONS='{"num_workers": 100}'
# in the bash shell to modify the number of workers using an environment
# variable. Keep your Python script exactly the same as exercise1a (in other
# words, you should NOT have any 'runner' section in your config.yaml). Re-run
# your script to validate the environment variable setting is now being used.

os.environ["NORNIR_RUNNER_OPTIONS"] = '{"num_workers": 100}'
nr = InitNornir(config_file="config.yaml")
print(f"Worker envvar count : {nr.config.runner.options['num_workers']}")

# 1d. Finally, modify the python script to set the number of workers to 15 using
# inline Python. Your inline Python should be similar to the following:
#
# nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})
#
# Re-run the script and confirm the number of workers is now 15.

nr = InitNornir(
    config_file="config.yaml",
    runner={"plugin": "threaded", "options": {"num_workers": 15}},
)
print(f"Worker inline count : {nr.config.runner.options['num_workers']}")
