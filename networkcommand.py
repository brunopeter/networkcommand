#!/usr/bin/env python
# Author:    Peter Bruno
# Purpose:   Script commands to group of Cisco devices with success/failure feedback.
from netmiko import ConnectHandler
from getpass import getpass
from tqdm import tqdm

# Save configuration when done.
WRITE_MEMORY = True

def usage() -> None:
    print("""
    ============================================================================================
    Purpose:
       networkcommand.py -- send command(s) to device(s) with visual feedback of progress.
    Requires:
       file 'cmdlist' containing commands to pass to devices.
       file 'devicelist' containing the ip addresses of devices to interact with.
    ============================================================================================
    """)
    exit()

def getfiledata(filename: str) -> tuple:
    """
        Generic function to open file and parse into lines
        returns tuple for memory conservation
    """
    inputlines = []
    try:
        with open(filename, "r") as f:
            inputlines = f.read().splitlines()
    except Exception as err:
        print(err)
        usage()
    return inputlines


def GetCredentials() -> str:
    """ Get username and password information. """
    print("Switch configuration updater. Please provide login information.\n")
    user = input("Username: ").strip()
    password = getpass("Password: ").strip()
    enable = getpass("Enable Secret: ").strip()

    return user, password, enable


def SwitchChanges(switch: dict) -> str:
    """ Connect to each switch and make configuration change(s). """
    # Print out the prompt/hostname of the device
    prompt = f"{switch.find_prompt():<40}"

    try:        # Ensure we are in enable mode and can make changes.
        switch.enable() if "#" not in prompt[-1] else None
    except Exception:
        prompt = prompt + "Unable to enter enable mode."
        exit
    else:
        try:
            output = switch.send_config_set(config_commands)
            if WRITE_MEMORY:
                output = switch.save_config()
        except Exception:       # Command failed! Stop processing further commands.
            prompt = prompt + "CHANGES FAILED!"
    return(prompt)


def DeviceUpdate(ciscosw: dict) -> None:
    """ Process devices and apply configuration changes. """

    # print headers for results output
    print(f"\n{'IP Address':<20}{'Switch Hostname':<40}")

    # parse list of switches and apply commands to them
    switch_tqdm = tqdm(switch_list, desc = "Processing...", position = 0)
    for switch_ip in switch_tqdm:
        ciscosw["ip"] = switch_ip
        try:    # Connect to switch and enter enable mode.
            switch_tqdm.set_description(f"Processing... {switch_ip:<20}")
            net_connect = ConnectHandler(**ciscosw)
            msg = SwitchChanges(net_connect) #, prompt)
            switch_tqdm.write(f"{switch_ip:<20}{msg}")
        except Exception:
            switch_tqdm.write(f"{switch_ip:<20}** Failed to connect.")
            continue

        net_connect.disconnect()
        switch_tqdm.set_description()


if __name__ == "__main__":
    try:
        config_commands = getfiledata("cmdlist") # Commands to issue
        switch_list = getfiledata("devicelist") # Devices to update
    except Exception:
        usage() # Error getting commands or devices, print usage and exit

    username, password, enasecret = GetCredentials()
    devicedict = {
        "device_type"   : "cisco_ios",
        "username"      : username,
        "password"      : password,
        "secret"        : enasecret,
        "ip"            : "",
    }

    DeviceUpdate(devicedict)
