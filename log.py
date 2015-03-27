#!/usr/bin/env python3.4
#encoding: utf-8

#backdoor: http://IP/web_shell_cmd.gch
#details: http://www.freebuf.com/news/58137.html

import sys
import time
import threading
from datetime import datetime

do_we_debug=True
res_file = 'res'

log_lock = threading.Lock()
def log(who,what):
    t = datetime.now()
    log_lock.acquire()
    msg = '{} {}: {}'.format(t, who, what)
    msg_with_crlf = '{} {}: {}\n'.format(t, who, what)
    if do_we_debug:
        print(msg)
    with open(res_file, 'a') as res_f:
        res_f.write(msg_with_crlf)
    res_f.close()
    log_lock.release()
    return
