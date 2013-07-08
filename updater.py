#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author:rikugun

import sys
import urllib
import os
from shutil import copyfile


HOSTS_URL='https://smarthosts.googlecode.com/svn/trunk/hosts'

LOCAL_HOSTS='/etc/hosts'

def main():
    #Try to gain root to operating /etc/ dir
    #os.system("sudo")
    if os.geteuid() != 0 :
        print "To modify hosts file need root premission"
        print "Please run again as \'sudo\'"
        sys.exit(1)
    copyfile(LOCAL_HOSTS,'hosts.bak')
    with open(LOCAL_HOSTS,'w') as hosts:
        hosts.write(os.linesep)
        for line in urllib.urlopen(HOSTS_URL):
            hosts.write(line.strip()+os.linesep)

    print "success!"

if __name__ == '__main__':
    if len(sys.argv)>1:
        HOSTS_URL = sys.argv[1]
    main()
