#!/usr/bin/env python

import subprocess
import argparse
import re
import sys


def get_arguments():
    # Create an object of the ArgumentParser class
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface",  # dest is the name of the variable that will be stored
                        help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac",
                        help="New MAC address")

    options = parser.parse_args()

    # Check if the user did not specify an interface
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options


# Function to change the MAC address
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    try:
        subprocess.run(["sudo", "ifconfig", interface, "down"])  # turn the interface down
        subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])  # gives the new MAC address
        subprocess.run(["sudo", "ifconfig", interface, "up"])  # bring the interface back up
    except subprocess.CalledProcessError:
        print("[-] An error occurred while changing the MAC address.")
        sys.exit(1)


# Function to get the current MAC address
def get_current_mac(interface):
    try:
        # Get the output of the ifconfig command
        ifconfig_result = subprocess.check_output(["ifconfig", interface])

        # Search for the MAC address in the ifconfig_result
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))

        # Check if a MAC address was found
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print("[-] Could not read MAC address.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("[-] An error occurred while getting the MAC address.")
        sys.exit(1)


args = get_arguments()

# Get the current MAC address
current_mac = get_current_mac(args.interface)
print("Current MAC = " + str(current_mac))
change_mac(args.interface, args.new_mac)

current_mac = get_current_mac(args.interface)

# Check if the MAC address was successfully changed
if current_mac == args.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
