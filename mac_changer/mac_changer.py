#!/usr/bin/env python
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (options, arguments) = parser.parse_args()  # returns the arguments and values entered in commandline
    if not options.interface:
        parser.error("[-] Please specify an interface , use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac addres , use --help for more info")
    return options

def change_mac(interface , new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    # second way of using subprocess avoiding input hijack
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    #print(ifconfig_result)

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                                          ifconfig_result)  # returns a group of matching object
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read Mac Address.") # return None if mac address not found

options = get_arguments()
interface = options.interface
new_mac = options.new_mac

current_mac = get_current_mac(interface)
print("[+] current MAC = "+str(current_mac))

change_mac(interface, new_mac)

current_mac = get_current_mac(interface)
if current_mac == new_mac:
    print("[+] MAC address was successfully changed to "+ current_mac)
else:
    print("[-] MAC address did not get changed")


# interface = input("interface > ") # raw_input() function
# new_mac = input("new MAC > ")
# subprocess.call("ifconfig "+ interface + " down", shell=True )
# subprocess.call("ifconfig "+ interface + " hw ether "+ new_mac, shell=True )
# subprocess.call("ifconfig "+ interface +" up", shell=True )