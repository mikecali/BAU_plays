#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, Will Thames <will@thames.id.au>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


#Github Repository here: https://github.com/willthames/ansible-testing/blob/master/test_tcp


DOCUMENTATION = '''
---
module: test_tcp
version_added: 1.5
short_description: Check if a tcp connection can be made
description:
  - Check if a TCP connection can be made to a host on a port
options: 
  host: 
    description:
    - host to connect to
    required: True
    default: null
  port:
    description: 
    - port to connect to
    required: True
    default: null
  state: 
    description: 
    - state of the port
    choices: [ 'open', 'closed' ]
    default: open
  timeout: 
    description:
    - time in seconds to wait for a response
    required: False
    default: 5
author: Will Thames
'''

EXAMPLES = '''
# Check if port 80 is open on a server
test_tcp: port=80 state=open timeout=10
'''
import socket

def main():
    module = AnsibleModule(
        argument_spec = dict(
            host=dict(required=True, default=None),
            port=dict(required=True, default=None),
            state=dict(choices=['open', 'closed'], default='open'),
            timeout=dict(required=False, default=5.0, type='float'),
        ),
        supports_check_mode=True
    )
    host = module.params.get('host')
    port = module.params.get('port')
    state = module.params.get('state')
    timeout = module.params.get('timeout')
    
    s = None
    for res in socket.getaddrinfo(module.params.get('host'), module.params.get('port'),
                                  socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try: 
            s = socket.socket(af, socktype, proto)
        except socket.error, msg:
            s = None
            continue
        try:
            s.settimeout(timeout)
            s.connect(sa)
        except socket.error, msg:
            s.close()
            s = None
            continue
        break
    
    if s is None:
        if state == 'open':
            module.fail_json(msg='Could not connect to %s on port %s' % (host, port))
        if state == 'closed':
            module.exit_json()
    else:
        if state == 'open':
            module.exit_json()
        if state == 'closed':
            module.fail_json(msg='Connection to %s on port %s should not have succeeded' % (host, port))
        s.close()

from ansible.module_utils.basic import *

main()
