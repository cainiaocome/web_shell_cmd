#!/usr/bin/env python3.4
#encoding: utf-8


import sys
import socket
import time
import requests
import threading
from datetime import datetime
from log import log

#headers is used so often, i include my firefox's here
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, utf-8',
            'Accept-Language':'en-US,en;q=0.5',
            'Connection':'keep-alive',
            'Host':'tieba.baidu.com',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140924 Firefox/24.0 Iceweasel/24.8.1'}

#a simple port probe implementation
def check_port(ip, port)
    try:
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.settimeout(2)
        result = sock.connect_ex( (str(ip), port) )
        if result == 0:
            sock.close()
            return True
    except:
        pass
    sock.close()
    return False
