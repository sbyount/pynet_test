#!/usr/bin/env python
'''
Use Paramiko to retrieve the entire 'show version' output.
'''

import paramiko
import time
from getpass import getpass

MAX_BUFFER = 65535

def clear_buffer(remote_conn):
    '''
    Clear any data in the receive buffer
    '''
    if remote_conn.recv_ready():
        return remote_conn.recv(MAX_BUFFER)

def disable_paging(remote_conn, cmd='terminal length 0'):
    '''
    Disable paging
    '''
    cmd = cmd.strip()
    remote_conn.send(cmd + '\n')
    time.sleep(1)
    clear_buffer(remote_conn)

def send_command(remote_conn, cmd='', delay=1):
    '''
    Send the command down the channel.
    Retrievel and return he output.
    '''
    if cmd != '':
        cmd = cmd.strip()

    remote_conn.send(cmd + '\n')
    time.sleep(delay)

    if remote_conn.recv_ready():
        return remote_conn.recv(MAX_BUFFER)
    else:
        return ''

def main():
    '''
    Retrieve show version output from pynet-rtr2
    '''
    ip_addr = '184.105.247.71'
    username = 'pyclass'
    password = getpass()
    port = 22

    # Create paramilo object
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.load_system_host_keys()

    # Trust SSH keys from remote device
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    remote_conn_pre.connect(ip_addr, port=port, username=username, password=password,
                            look_for_keys=False, allow_agent=False)
    # Create shell object
    remote_conn = remote_conn_pre.invoke_shell()

    time.sleep(1)
    clear_buffer(remote_conn)
    disable_paging(remote_conn)

    output = send_command(remote_conn, cmd='show version')
    print '\n>>>>>'
    print output
    print '\n>>>>>'

if __name__ == '__main__':
    main()
