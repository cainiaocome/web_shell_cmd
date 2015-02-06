#!/usr/bin/env python
#encoding: utf-8


#backdoor: http://IP/web_shell_cmd.gch
#details: http://www.freebuf.com/news/58137.html

import sys
import netaddr
import time
import requests
import threading
import gc
import objgraph
from datetime import datetime

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, utf-8',
            'Accept-Language':'en-US,en;q=0.5',
            'Connection':'keep-alive',
            'Host':'tieba.baidu.com',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140924 Firefox/24.0 Iceweasel/24.8.1'}
log_lock = threading.Lock()
def log(who,what):
    t = datetime.now()
    log_lock.acquire()
    msg = '{} {}: {}'.format(t, who, what)
    msg_with_crlf = '{} {}: {}\n'.format(t, who, what)
    #print msg
    with open('web_shell_cmd.res', 'a') as res_f:
        res_f.write(msg_with_crlf)
    res_f.close()
    log_lock.release()
    return

d_lock = threading.Lock()
def debug():
    d_lock.acquire()
    gc.collect()
    objgraph.show_most_common_types(limit=10)
    d_lock.release()
    return

class probe(threading.Thread):
    
    def __init__(self, name, cidr):
        threading.Thread.__init__(self)
        self.name = name
        self.cidr = cidr

    def run(self):
        global headers
        log(self.name, 'started')
        self.ip_cidr_list = list(netaddr.IPNetwork(self.cidr))
        for self.ip in self.ip_cidr_list:
            if self.ip.is_unicast() and not self.ip.is_private():
                self.url = 'http://{}/web_shell_cmd.gch'.format(str(self.ip))
                try:
                    #log(self.name, url)
                    self.res = requests.get(url=self.url, timeout=3, headers=headers)
                except Exception,e:
                    #log(self.name,'{} {} {}'.format(Exception,':',e))
                    continue
                else:
                    if self.res.status_code==requests.codes.ok:
                        log(self.name,'{} is vulnable!'.format(self.ip))
        self.stop()
        return

    def stop(self):
        self.thread_stop = True
        
i = 0
f = open('ip.china','r')
while True:
    while threading.active_count()>=50:
        time.sleep(3)
    line = f.readline()
    if len(line)==0:
        break
    new_thread = probe(str(i), line)
    new_thread.start()
    i = i + 1

time.sleep(3600)
sys.exit(0)
