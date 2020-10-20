#!/usr/bin/env python
# this allow to cut internet connection from any client
# by creating a queue list of requests packet that you could modify
# iptables -I FORWARD -j NFQUEUE --queue-num 0 to create a queue 0 on linux, FORWARD chain for remote computer, OUTPUT/INPUT chain for local computer
# iptables --flush to delete the iptable

import netfilterqueue

def process_packet(packet): # packet present in the queue
   print(packet)
   packet.drop() # to drop the packet in the queue or
   packet.accept() # to forward packet in the queue


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
# connect the queue 0 created with iptable and netfilterquue, #
# process_packet is callback function executed on each packet in the queue
queue.run() # to run the queue

