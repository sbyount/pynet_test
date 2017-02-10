#!usr/bin/env python

import pexpect
from getpass import getpass
import sys

def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    port = 22
    password = '88newclass'

    ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip_addr, port))

    #ssh_conn.logfile = sys.stdout
    ssh_conn.timeout = 3
    ssh_conn.expect('ssword:')
    ssh_conn.sendline(password)
    ssh_conn.expect('#') #regular expression
    #print ssh_conn.before

    #router_name = ssh_conn.before
    #router_name = router_name.strip()
    #prompt = router_name + ssh_conn.after
    #prompt = prompt.strip()

    ssh_conn.sendline('sh ip int br\n')
    ssh_conn.expect('#') #regular expression
    #ssh_conn.expect(prompt)
    print ssh_conn.before
    #print ssh_conn.after


if __name__ == '__main__':
    main()
