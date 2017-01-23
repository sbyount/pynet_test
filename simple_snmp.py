COMMUNITY_STRING = 'galileo'
SNMP_PORT = 161
IP = '84.105.247.70'

# tuple - unchangeable, no adds or updates
a_device =  (IP, COMMUNITY_STRING, SNMP_PORT)

from snmp_helper import snmp_get_oid, snmp_extract

OID = '1.3.6.1.2.1.1.1.0'

# get the data from the router (hex)
snmp_data = snmp_get_oid(a_device, oid=OID)

ouput = snmp_extract(snmp_data)
