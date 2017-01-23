'''
Connect to pynet-rtr1 and pynet-rtr2 using SNMP
Print out MIB2 sysName and sysDescr
'''

import snmp_helper

SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'

def main():

    ip1 = '184.105.247.70'
    ip2 = '184.105.247.71'

    community_string = 'galileo'

    rtr1 = (ip1, community_string, 161)
    rtr2 = (ip2, community_string, 161)

    for a_device in (rtr1, rtr2):
        print
        for the_oid in (SYS_NAME, SYS_DESCR):
            snmp_data = snmp_helper.snmp_get_oid(a_device, oid=the_oid)
            output = snmp_helper.snmp_extract(snmp_data)

            print output
        print

if __name__ == '__main__':
    main()
