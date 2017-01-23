#  script to connect to pynet_rtr1, and return sh ip int br

import telnetlib
import sys
import socket
import time

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def send_comand(remote_conn, cmd):
    cmd = cmd.rstrip() #strip off any newlines
    remote_conn.write(cmd + '\n')
    time.sleep(1)
    return remote_conn.read_very_eager()

def login(remote_conn, username, password):
    output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
    remote_conn.write(username + '\n')
    output += remote_conn.read_until("assword:", TELNET_TIMEOUT)
    remote_conn.write(password + '\n')
    return output

def telnet_connect(ip_addr):
    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        sys.exit("\nConnection Failed\n")

def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'

    remote_conn = telnet_connect(ip_addr)
    output = login(remote_conn, username, password)

    time.sleep(1)
    output = remote_conn.read_very_eager()

    # Disable paging and show version
    output = send_comand(remote_conn, 'terminal length 0')
    output = send_comand(remote_conn, 'show ip int br')
    print output

    remote_conn.close()

if __name__ == '__main__':
	main()
