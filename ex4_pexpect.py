#!/usr/bin/env python
'''
Use pexpect to get sh ip int br from pynet-rtr2
This code does not run
'''

import pexpect
from getpass import getpass
import time

def login(ssh_conn):
    '''
    Handle sending password
    '''
    password = getpass()

    ssh_conn.expect('ssword:')
    ssh_conn.sendline(password)
    ssh_conn.expect('#')

def find_prompt(ssh_conn):
    '''
    Find the current prompt
    Pexpect is non-greedy which is problematic
    '''
    ssh_conn.send('\n')
    time.sleep(1)
    ssh_conn.expect('#')
    prompt = ssh_conn.before + ssh_conn.after
    return prompt.strip()

def disable_paging(ssh_conn, pattern='#', cmd='terminal length 0'):
    '''
    Disable the paging of output i.e. --More--
    '''
    ssh_conn.sendline(cmd)
    ssh_conn.expect(pattern)

def main():
    # pynet-rtr2
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    port = 22

    ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip_addr, port))
    ssh_conn.timeout = 3

    login(ssh_conn)
    prompt = find_prompt(ssh_conn)
    disable_paging(ssh_conn, prompt)

    ssh_conn.sendline('config t')
    ssh_conn.expect('#')

    ssh_conn.sendline('logging buffer 9000')
    ssh_conn.expect('#')

    ssh_conn.sendline('end')
    ssh_conn.expect(prompt)

    ssh_conn.sendline('show run | inc logging buffer')
    ssh_conn.expect(prompt)


    print
    print ssh_conn.before
    print

if __name__ == '__main__':
    main()
