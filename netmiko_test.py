#!usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass

#passowrd = getpass()

pynet1 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.70',
    'username': 'pyclass',
    'password': '88newclass'
}

pynet_rtr1 = ConnectHandler(**pynet1) # Pass all args from the dictionary

outp = pynet_rtr1.send_command('sh ip int br')
print outp
    
