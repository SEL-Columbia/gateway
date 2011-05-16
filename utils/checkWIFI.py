
"""Cron job to check wifi server every hour"""
__author__ = "Ivan Willig"
import urllib
from datetime import datetime

wifi_address = 'http://41.223.84.25'
logs = open('wifi_access.log', 'a')

now = datetime.now().ctime()
if __name__ == '__main__':
    try:
        logs.write('sucess:%s,date:%s\n' % (urllib.urlopen(wifi_address),
                                             now))
    except Exception as e:
        logs.write('error:%s,date:%s\n' % (e, now))
