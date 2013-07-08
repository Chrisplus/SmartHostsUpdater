#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author:rikugun

import sys
import urllib
import os
from shutil import copyfile


HOSTS_URL='https://smarthosts.googlecode.com/svn/trunk/hosts'
HOSTS_URL_USA = "https://smarthosts.googlecode.com/svn/trunk/hosts_us"

LOCAL_HOSTS='/etc/hosts'

def main():
    # Try to gain root to operating /etc/ dir
    # os.system("sudo")
    if os.geteuid() != 0 :
        print "To modify hosts file need root premission"
        print "Please run again as \'sudo\'"
        sys.exit(1)

    # Gain the root premission and start operating

    # Backup the older hosts file
    print "Backup the older hosts file in \'/etc/hosts.bak\'"
    copyfile(LOCAL_HOSTS,'/etc/hosts.bak')
    print "Start checking update"

    statusCode = False
    with open(LOCAL_HOSTS,'w') as hosts:
        hosts.write(os.linesep)
        netHosts = urllib.urlopen(HOSTS_URL)

        # When retryTime is negative, it means pull content successfully.
        retryTime = 0;

        while retryTime < 2:
            if netHosts.getcode() != 200:
                ++retryTime
                continue
            else:
                retryTime = -1
                break

        if retryTime == -1:
            # Pull content successfully
            print "The lastest hosts version:"
            print netHosts.readline()
            for line in urllib.urlopen(HOSTS_URL):
                hosts.write(line.strip()+os.linesep)
            statusCode = True
        elif retryTime >= 2:
            # Retry failed
            print "Can not access update file now, check your internet setting and try again later"
        else:
            print "Unknown error occur"

    if statusCode:
        print "Hosts file update successfully! Enjoy it."
    else :
        print "Hosts file update failed, try again later."


if __name__ == '__main__':
    if len(sys.argv)>1:
        HOSTS_URL = sys.argv[1]
    main()
