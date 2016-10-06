#!/usr/bin/env python

import json
import simplejson as json
HAS_PYSPHERE_MODULE = True
try:
    from pysphere import VIServer, VIProperty, MORTypes
    from pysphere import VIException, VIApiException, FaultTypes
except ImportError:
    HAS_PYSPHERE_MODULE = False
from ansible.module_utils.basic import * 

DOCUMENTATION = '''
---
module: vm_snapshot
short_description: Creates a snapshot for a VM.
description:
     - Connect with the Vsphere environment and create a snapshot for a VM specified
version_added: "1.0"
options:
  vcenter_hostname:
    description:
      - The hostname of the vcenter server the module will connect to, to create the guest.
    required: true
    default: null
    aliases: []
  user:
    description:
      - username of the user to connect to vcenter as.
    required: true
    default: null
  password:
    description:
      - password of the user to connect to vcenter as.
    required: true
    default: null
  cluster:
    description:
      - The name of the cluster to create the VM in. By default this is derived from the host you tell the module to build the guest on.
    required: false
    default: None
  datacenter:
    description:
      - The name of the datacenter to create the VM in.
    required: true
    default: null

'''
def connect_VI(vcenter_hostname, user, password):
    # Create the connection to vCenter Server
    server = VIServer()
    try:
        server.connect(vcenter_hostname, user, password)
    except VIApiException, err:
        module.fail_json(msg="Cannot connect to %s: %s" % (vcenter_hostname, err))
    return server



def take_snapshot(server,vm_name,snapshot_name,description):
    vm = server.get_vm_by_name(name=vm_name)
    if vm:
        vm.create_snapshot(name=snapshot_name,description=description,memory=False)
    else:
        module.fail_json(msg="Cannot take a snapshot for %s: %s" % (vm_name, err))


def main():
    module = AnsibleModule(
        argument_spec = dict(
            vcenter_hostname     = dict(required=True, type='str'),
            user                 = dict(required=True, type='str'),
            password             = dict(required=True, type='str'),
            cluster              = dict(required=False, default=None, type='str'),
            datacenter           = dict(required=False, default=None, type='str'),
            vm_name              = dict(required=True, type='str'),
        ),
        supports_check_mode = False,
    )
    
    if not HAS_PYSPHERE_MODULE:
        module.fail_json(msg="pysphere is not installed")

    vcenter_hostname  = module.params['vcenter_hostname']
    user = module.params['user']
    password = module.params['password']
    datacenter = module.params['datacenter']
    vm_name = module.params['vm_name']



    s = connect_VI(vcenter_hostname,user,password)
    results = take_snapshot(s,vm_name,"Pre-patch","Pre-patching Snapshot")
    print results
    module.exit_json(changed=True)


main()
