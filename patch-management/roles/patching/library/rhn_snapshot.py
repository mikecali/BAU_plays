#!/usr/bin/env python


import json
import simplejson as json
import sys
import time
import xmlrpclib
from ansible.module_utils.basic import *

DOCUMENTATION = ''' 
---
module: vsphere_guest
short_description: Creates a Satellite snapshot for servers
description:
     - Communicates with Redhat Satellite, creating a server snapshot
version_added: "0.1"
options:
  satellite_url:
    description:
      - The URL of the satellite you are connection to.
    required: true
    default: null
    aliases: []
  username:
    description:
      - username of the user to connect to satellite as.
    required: true
    default: null
  password:
    description:
      - password of the user to connect to satellite as.
    required: true
    default: null
  hostname:
    description:
      - The name of the hostname to create the snapshot for.
    required: false
    default: None
'''

def get_sat_session(satellite_url, user_name, password):
    try:

        client = xmlrpclib.Server(satellite_url, verbose=3)
        key = client.auth.login(user_name, password)
    except xmlrpclib.ProtocolError as e:
        print("xmlrpc protcol error: %s : %s",
                            e.errcode, e.errmsg)
    return (client, key)


def get_sys_id(client, key,  hostname):

    '''this function returns the internal RHSS system ID which is used
     to reference hosts managed by the satellite server'''

    rhn_sys_id = client.system.getId(key, hostname)
    sys_id = rhn_sys_id[0]['id']
    return sys_id


def rhss_create_rollback_tag(client, key, hostname):
    '''Create a rollback tag in satellite for the host being patched'''
    server_id = get_sys_id(client, key,  hostname)
    tagname = 'Ansible-%s' % time.time()
    result = client.system.tagLatestSnapshot(key, server_id, tagname)
    return result



def main():
    module = AnsibleModule(
        argument_spec = dict(
            satellite_url        = dict(required=True, type='str'),
            user_name            = dict(required=True, type='str'),
            password             = dict(required=True, type='str'),
            hostname             = dict(required=True, type='str'),
        ),
        supports_check_mode = False,
        required_together = [ ['resource_pool','cluster'] ],
    )


    satellite_url = module.params['satellite_url']
    user_name = module.params['user_name']
    password = module.params['password']
    hostname = module.params['hostname']


# Connection to the Satellite

    client,key = get_sat_session(satellite_url,user_name,password)
    results = rhss_create_rollback_tag(client,key,hostname)
    if results == 1:
    	module.exit_json(changed=True)
    else:
        module.exit_json(changed=false)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


