#!/usr/bin/env python
""" ssh to an ansible host using all ansible's connection info.

    Usage:
        ansible-ssh [-i inventory_path] hostname [command]
"""
from __future__ import print_function

__version__ = "0.0"

import sys, json, subprocess, collections

def main():

    # parse command-line
    opts = {'-i':'/etc/ansible/hosts'}
    opts.update([(v, sys.argv[i + 1]) for (i, v) in enumerate(sys.argv[1:], 1) if v.startswith('-')])
    #print('opts:', opts)
    inventory_path = opts['-i']
    args = [v for (i, v) in enumerate(sys.argv[1:]) if (v not in opts.keys() and v not in opts.values())]
    #print('args:', args)
    if len(args) == 0:
        exit('ERROR: must provide a hostname')
    if len(args) == 1:
        hostname = args[0]
        remote_cmd = None
    elif len(args) == 2:
        hostname, remote_cmd = args
    else:
        exit('ERROR: too many arguments')
    
    # read inventory info:
    host_info = subprocess.check_output(('ansible-inventory', '-i', inventory_path, '--host', hostname))
    h =  json.loads(host_info)
    # e.g. ssh -o ProxyCommand="ssh centos@128.232.226.6 -W %h:%p" centos@128.232.226.6
    ssh_cmd = ['ssh', h['ansible_ssh_common_args'], '%s@%s' % (h['ansible_user'], h['ansible_host'])]
    if remote_cmd is not None:
        ssh_cmd += [remote_cmd]
    ssh_cmd_str = ' '.join(ssh_cmd) # because common_args is already multiple args.
    print('running', ssh_cmd_str)
    subprocess.call(ssh_cmd_str, shell=True)
    #print host_info

if __name__=='__main__':
    main()