# networkcommand
A short script to automate changes to multiple devices.  Useful for quick changes to multiple devices.

To use this script:
* modify the 'config_commands' tuple to contain all of the command(s) you want applied to the devices.
* modify the 'switch_list' tuple to contain the ip address of the devices

User will be prompted for a login name, password and an enable password (optional).

Devices will be connected to one at at time, the commands issued and feedback provided to the screen on progress, success and failure.
