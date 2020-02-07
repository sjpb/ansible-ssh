#!/usr/bin/env python
""" ssh to an ansible host using all ansible's connection info.

    Usage:
        ansible-ssh inventory_path hostname
"""
from __future__ import print_function

__version__ = "0.0"

import sys, json, subprocess

def main():
    inventory_path, hostname = sys.argv[1:]
    host_info = subprocess.check_output(('ansible-inventory', '-i', inventory_path, '--host', hostname))
    h =  json.loads(host_info)
    # ssh -o ProxyCommand="ssh centos@128.232.226.6 -W %h:%p" centos@128.232.226.6
    ssh_cmd = ('ssh', h['ansible_ssh_common_args'], '%s@%s' % (h['ansible_user'], h['ansible_host']))
    ssh_cmd_str = ' '.join(ssh_cmd) # because common_args is already multiple args.
    print('running', ssh_cmd_str)
    subprocess.call(ssh_cmd_str, shell=True)
    #print host_info

if __name__=='__main__':
    main()