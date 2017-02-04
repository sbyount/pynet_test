#!/usr/bin/env python

# imports
import cPickle as pickle
import os.path
from getpass import getpass
from datetime import datetime
from snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail

# contstants

# SNMP constant assignments
RUN_LAST_CHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'
SYS_UPTIME = '1.3.6.1.2.1.1.3.0'
# 300 seconds (converted to hundredths of seconds)
RELOAD_WINDOW = 300 * 100
DEBUG = True


# Get saved objects using pickle
def obtain_saved_objects(file_name):
    '''
    Read in saved objects from pickle file.
    Return them as a dictionary.
    '''

    # check to see if the file exists
    if not os.path.isfile(file_name):
        return {}

    # read in saved network devices
    net_devices = {} #initialize the dictionary
    with open(file_name, 'r') as f:
        while True:
            try:
                tmp_device = pickle.load(f)
                net_devices[tmp_device.device_name] = tmp_device
            except EOFError:
                break

    return net_devices

# send notification
def send_notification(net_device):
    '''
    Send email notification about modified device.
    '''
    current_time = datetime.now()

    sender = 'sbyount@satx.rr.com'
    recipient = 'sbyount@satx.rr.com'
    subject = 'Device {0} was modified'.format(net_device.device_name)

    message = '''
The running configuration of {0} was modified.
This change was detected at {1}
'''.format(net_device.device_name, current_time)

    if send_mail(recipient, subject, message, sender):
        print "Email notification sent to {}".format(recipient)
        return True

# network device objects
class NetworkDevice(object):
    '''
    Object to store network device information
    '''
    def __init__(self, device_name, uptime, last_changed, config_changed=False):
        self.device_name = device_name
        self.uptime = uptime

        # The updtime value in hundredths of seconds when it was last changed
        self.last_changed = last_changed
        self.run_config_changed = config_changed

# main function
def main():
    '''
    Check if the running-configuration has changed, send an email notification when
    this occurs.
    '''
    # pickle file that stores previous running config last changed time stamp
    net_dev_file = 'netdev.pkl'

    # SNMP connection parameters
    rtr1_ip_addr = '184.105.247.70'
    rtr2_ip_addr = '184.105.247.71'
    my_key = 'galileo1' #not using getpass

    a_user = 'pysnmp'
    auth_key = my_key
    encrypt_key = my_key

    snmp_user = (a_user, auth_key, encrypt_key)
    pynet_rtr1 = (rtr1_ip_addr, 161)
    pynet_rtr2 = (rtr2_ip_addr, 161)

    print '\n*** Checking for device changes ***'
    saved_devices = obtain_saved_objects(net_dev_file)
    print '{0} devices were previously saved\n'.format(len(saved_devices))

    # temporarily store the current devices in a dictionary
    current_devices = {}

    # Connect to each device and get last changed time
    for a_device in (pynet_rtr1, pynet_rtr2):
        snmp_results = []
        for oid in (SYS_NAME, SYS_UPTIME, RUN_LAST_CHANGED):
            try:
                value = snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=oid))
                snmp_results.append(int(value))
            except ValueError:
                snmp_results.append(value)
        device_name, uptime, last_changed = snmp_results
        if DEBUG:
            print '\nConnected to device = {0}'.format(device_name)
            print 'Last changed timestamp = {0}'.format(last_changed)
            print 'Uptime = {0}'.format(uptime)

        # See if the device has been previously saved
        if device_name in saved_devices:
            saved_device = saved_devices[device_name]
            print "{0} {1}".format(device_name, (35 - len(device_name))*'.'),

            # Check for a reboot, did uptiome decrease or last_changed decrease?
            if uptime < saved_device.uptime or last_changed < saved_device.last_changed:
                if last_changed <= RELOAD_WINDOW:
                    print "DEVICE RELOADED...not changed"
                    current_devices[device_name] = NetworkDevice(device_name, uptime,
                    last_changed, False)

                else:
                    print 'DEVICE RELOADED...and changed'
                    current_devices[device_name] = NetworkDevice(device_name, uptime,
                    last_changed, True)

                    send_notification(current_devices[device_name])

            elif last_changed == saved_device.last_changed:
                # Running config last changed is the sysName
                print 'Not changed'
                current_devices[device_name] = NetworkDevice(device_name, uptime,
                last_changed, False)

            elif last_changed > saved_device.last_changed:
                # running config was modified
                print "CHANGED"
                current_devices[device_name] = NetworkDevice(device_name, uptime,
                last_changed, True)

            else:
                raise ValueError()

        else:
            # New device, just save it
            print "{0} {1}".format(device_name, (35 - len(device_name))*'.'),
            print 'Saving new device'
            current_devices[device_name] = NetworkDevice(device_name, uptime,
            last_changed, False)

    # Write devices to a pickle file
    with open(net_dev_file, 'w') as f:
        for dev_obj in current_devices.values():
            pickle.dump(dev_obj, f)
    print

if __name__ == '__main__':
    main()
