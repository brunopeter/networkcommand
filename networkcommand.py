#!/usr/bin/env python
# Author:    Peter Bruno
# Purpose:   Script commands to group of Cisco devices with success/failure feedback.
from netmiko import ConnectHandler
from getpass import getpass

# Commands to issue on each switch
config_commands = tuple(filter(lambda x: x.strip() != '', '''
no snmp-server community private
no snmp-server community public
'''.splitlines()))

# List of switches to update.  Parse into a list and remove any blanks.
switch_list = tuple(filter(lambda x: x.strip() != '', '''
192.168.1.11
192.168.1.12
'''.splitlines()))

# Save configuration when done.
WRITE_MEMORY = True


def GetCredentials():
    """ Get username and password information. """
    print("Switch configuration updater. Please provide login information.\n")
    usr = input("Username: ")
    pwd = getpass("Password: ")
    ena = getpass("Enable Secret: ")

    return usr.strip(), pwd.strip(), ena.strip()


def SwitchChanges(switch):
    """ Connect to each switch and make configuration change(s). """
    # Print out the prompt/hostname of the device
    prompt = switch.find_prompt()

    print(f"{prompt:<40}", end="", flush=True)
    try:        # Ensure we are in enable mode and can make changes.
        switch.enable() if "#" not in prompt[-1] else None
        print("#", end="", flush=True)
    except Exception:
        print("Unable to enter enable mode.", end="", flush=True)
        exit
    else:
        try:
            output = switch.send_config_set(config_commands)
            print(f"*", end="", flush=True)
            if WRITE_MEMORY:
                output = switch.save_config()
                print(f"w", end="", flush=True)
        except Exception:       # Command failed! Stop processing further commands.
            print("FAILED!")


def DeviceUpdate():
    """ Parse list of switches """
    username, password, enasecret = GetCredentials()
    ciscosw = {
        "device_type"   : "cisco_ios",
        "username"      : username,
        "password"      : password,
        "secret"        : enasecret,
    }

    # print headers
    print(f"\n{'IP Address':<20}{'Switch Hostname':<40}{'Results':<20}", end="")

    # parse list of switches and apply commands to them
    for switch_ip in switch_list:
        ciscosw["ip"] = switch_ip
        print(f"\n{switch_ip:<20}", end="", flush=True)
        try:    # Connect to switch and enter enable mode.
            net_connect = ConnectHandler(**ciscosw)
            SwitchChanges(net_connect)
        except Exception:
            print(f"** Failed to connect.", end="", flush=True)
            continue

        net_connect.disconnect()


def main():
    DeviceUpdate()
    print(f"\n All Done!")


if __name__ == "__main__":
    main()
