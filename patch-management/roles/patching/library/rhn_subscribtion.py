#!/usr/bin/env python


from ansible.module_utils.basic import *
import rhn_snapshot

DOCUMENTATION = '''
---
module: rhn_subscription
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
      - The name of the hostname to change subscription for.
    required: true
    default: None
  Channel:
    description:
      - The name of the channel to subscribe to.
    required: true
    default: None
'''


def validate_channel(client, key, sys_id):

    channel_list = client.system.listSubscribableBaseChannels(key, sys_id)
    if channel_list[0]['id']:
        return True
    else:
        return False


def set_base_channel(client, key, sys_id, channel_name):
    results = client.system.setBaseChannel(key, sys_id, channel_name)




def main():
    module = AnsibleModule(
        argument_spec = dict(
            satellite_url        = dict(required=True, type='str'),
            user_name            = dict(required=True, type='str'),
            password             = dict(required=True, type='str'),
            hostname             = dict(required=True, type='str'),
            channel              = dict(required=True, type='str'),

        ),
        supports_check_mode = False,

    )

    satellite_url = module.params['satellite_url']
    user_name = module.params['user_name']
    password = module.params['password']
    hostname = module.params['hostname']
    channel = module.params['channel']

# Connection to the Satellite
    client, key = rhn_snapshot.get_sat_session(satellite_url, user_name, password)
    sys_id = rhn_snapshot.get_sys_id(client, key, hostname)
    results = validate_channel(client,key,sys_id)
    if results:
        set_base_channel(client,key,sys_id,channel)
        module.exit_json(changed=True)
    else:
        module.exit_json(changed=False)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


