#!usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
from test_devices import pynet2

def main():
    '''
    Using Netmiko to change the logging buffered size on pynet-rtr2
    '''
    password = getpass()
    pynet2['password'] = password

    net_connect = ConnectHandler(**pynet2)
    config_commands = ['logging buffered 20000']
    net_connect.send_config_set(config_commands)

    outp = net_connect.send_command('show run | inc logging buffer')

    print '>' * 80
    print "Device: {}:{}".format(net_connect.ip, net_connect.port)
    print outp
    print '<' * 80

if __name__ == '__main__':
    main()
