#!usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
from test_devices import pynet1, pynet2, juniper_srx

def main():
    '''
    Using Netmiko enter into configuration mode on a network device.
    Verify that you are currently in configuration mode.
    '''
    password = getpass()

    for a_dict in (pynet1, pynet2, juniper_srx):
        a_dict['password'] = password

    net_connect2 = ConnectHandler(**pynet2)
    net_connect2.config_mode() # enter config mode

    print
    print "Checking pynet-rtr2 in config mode"
    print "Config mode check: {}".format(net_connect2.check_config_mode())
    print "Current prompt: {}".format(net_connect2.find_prompt())
    print

if __name__ == '__main__':
    main()
