import telnetlib
import time

IP = '184.105.247.70'
PORT = 23
TIMEOUT = 6

username = 'pyclass'
password = '88newclass'


# get connection with IP, port and timeout
my_conn = telnetlib.Telnet(IP, PORT, TIMEOUT)

# send username and password
output = my_conn.read_until('sername:', TIMEOUT)
my_conn.write(username + '\n')
output = my_conn.read_until('assword:', TIMEOUT)
my_conn.write(password + '\n')

output = my_conn.read_very_eager()

# Disable paging and show version
output = my_conn.write('term len 0' + '\n')
output = my_conn.write('sh ip int br' + '\n')
time.sleep(1)
output = my_conn.read_very_eager()

print output

my_conn.close()
