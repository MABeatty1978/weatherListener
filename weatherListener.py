#!/usr/bin/python3
import socket
import select
import time
import struct
import pprint
import json
from datetime import datetime
import requests


# create broadcast listener socket
def create_broadcast_listener_socket(broadcast_ip, broadcast_port):

    b_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    b_sock.bind(('', broadcast_port))

    mreq = struct.pack("4sl", socket.inet_aton(broadcast_ip), socket.INADDR_ANY)
    b_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return b_sock



# ip/port to listen to
BROADCAST_IP = '239.255.255.255'
BROADCAST_PORT = 50222

# create the listener socket
sock_list = [create_broadcast_listener_socket(BROADCAST_IP, BROADCAST_PORT)]

while True:
    # small sleep otherwise this will loop too fast between messages and eat a lot of CPU
    time.sleep(0.01)

    # wait until there is a message to read
    readable, writable, exceptional = select.select(sock_list, [], sock_list, 0)

    # for each socket with a message
    for s in readable:
        data, addr = s.recvfrom(4096)

        # convert data to json
        d = json.loads(data)
        print(d)
        if d['type'] == 'evt_strike':
            last_strike_time = d['evt'][0]
            last_strike_dist = d['evt'][1]
            last_strike_energy = d['evt'][2]
            recentStrike = True
            print("********EVENT STRIKE********")
            print("Last Strike Time: " + datetime.fromtimestamp(last_strike_time).strftime("%m/%d %I:%M:%S%p"))
            print("Last Strike Dist: " + str(last_strike_dist))
            print("Last Strike Engy: " + str(last_strike_energy))
        elif d['type']  == 'evt_precip':
            print(d)

