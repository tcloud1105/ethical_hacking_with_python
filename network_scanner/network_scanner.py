#!/usr/bin/env python

import scapy.all as scapy
import pprint, argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP/ IP Range")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip) # arp packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Ethernet packet
    arp_request_broadcast = broadcast/arp_request # combination of arp and ethernet packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac":element[1].hwsrc}
        client_list.append(client_dict)
        #print(element)
        #print(element[1].show())
    return client_list

    # answered_list , unanswered_list = scapy.srp(arp_request_broadcast, timeout=1) # srp stands for send and receive packet and returns tuple value
    # print(answered_list.summary())
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    # print(broadcast.summary())
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP()) # to learn fields of ARP class
    # scapy.ls(scapy.Ether())
    # scapy.arping(ip)

def print_result(results_list):
    print("IP\t\t\tMAC ADDRESS\n------------------------------------------")
    for client in results_list:
        print(client["ip"] +"\t\t"+ client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)