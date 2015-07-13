import os
import re
import datetime as dt

def stamp():
    now = dt.datetime.now()
    stamp = str(now.date())+'.'+str(now.time()).split('.')[0]
    return stamp

def fileage(trgfile):
    timefile = '/tmp/thetime'
    trgtime = os.stat(trgfile).st_mtime
    with open(timefile, 'w+'):
        thetime = os.stat(timefile).st_mtime
    os.remove(timefile)
    return int(str(((thetime-trgtime))).split('.')[0])

