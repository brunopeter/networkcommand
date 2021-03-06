[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/brunopeter/networkcommand)

# Simple Network Command
A short script to automate changes to multiple devices.  Useful for quick changes when a another management tool may be overkill.

## networkcommand

To use this script:
Two supporting files are required with a list of commands and devices.
* file: "cmdlist" containing list of command(s)
* file: "devicelist" containing list of device(s)

# Explaination
User will be prompted for a login name, password and an enable password (optional).  It is assummed that the same credentials are valid for all of the devices.

Devices will be connected to one at at time, the commands issued and feedback provided to the screen on progress, success and failure.  There is no automatic rollback for failed / partial changes.

# Examples
## Example execution:
```
python networkcommand.py

Switch configuration updater. Please provide login information.

Username: cisco
Password:
Enable Secret:

IP Address          Switch Hostname                         Results
192.168.1.11        switch1>                                #**w
192.168.1.12        switch2>                                #**w
```

## Supporting files:

file:  cmdlist
```
no snmp-server community public
no snmp-server community private
```

file:  devicelist
```
192.168.1.11
192.168.1.12
```

# Installation
This has been tested using on python 3.8.6 & 3.9 on Windows X, but should work on most operating systems.

```
git clone https://github.com/brunopeter/networkcommand.git
cd networkcommand
pip install -r requirements.txt
```


## Requirements
* netmiko >= 2.7.1
* tqdm >= 4.56.0