#!/usr/bin/python
'''This module contains functions used for talking with check_MK livestatus
Can set downtime, remove downtime, and check for any critial errors'''
# Nagios downtime and status checks, using livestatus
# This module also handles logging functions for the main project.

# AUTHOR: Steve Foris (steve.foris@datacom.co.nz)
# DATE: 2015/10/19

#TODO - make another call to livestatus to check  downtime flag has been properly set.

import sys
import socket
import time

#project modules
import config
from ansible.module_utils.basic import *
DOCUMENTATION = '''
---
module: monitoring.py
short_description: Enable or disable monitored services
description:
     - Mainly used for patching and to schedule a downtime to servers and disable monitoring
version_added: "0.1"
options:
  cmk_server:
    description: The nagios server
    required: true
    default: null
  cmk_port:
    description: The post number that will be used for communications , defaults to 6557
    required: true
    default: true
requirements: [ ]
'''

#The class below could just be defined as a dict, using a class to add further
#capability in the future if required.

verbose = False
class CmkObject(object):
    '''class to hold information on the CMK object, currently only used to
    store data, addtional methods may be added later'''
    def __init__(self, cmk_server, cmk_server_port, hostnames,
                message="automatic patching"):
        self.cmk_server = cmk_server
        self.cmk_server_port = cmk_server_port
        self.hostnames = hostnames
        self.message = message

def init_sock(cmk_server, cmk_server_port=6557):
    '''Initlize a socket to talk with the CMK server, takes a server / ip and
    port as arguments, and returns a socket, by default the live status
    agent listens on tcp port 6557'''
    #TODO - add try / except
    client_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((cmk_server, cmk_server_port))
    return client_socket

def clean_sock(client_socket):
    #TODO: Futher clean up code may be required, also add try / except.
    '''cleanly close the socket'''
    client_socket.close()

def send_cmk_cmds(CmkObject, cmd_list):
    #TODO: needs try / except
    client_socket = init_sock(CmkObject.cmk_server, CmkObject.cmk_server_port)
    '''Create a socket and send a list of commands to the livestatus server'''
    config.logger.debug("Sending CMK message %s", cmd_list)
    for cmd in cmd_list:
        client_socket.sendall(cmd)
    return client_socket

def set_notification_state(CmkObject, action):

    if config.dryrun:
        config.logger.info('running in drymode, no change to monitoring state')
    else:
        #This function is used to set or remove downtime for specified hosts.
        cmd_list = []
        if action == 'disable':
            config.logger.info("Disabling notifications for host(s): %s",\
                                CmkObject.hostnames)
            #hardcoded value of 28800 is for 8 hours, this long period is used
            #because we explicitly remove the downtime when completed.
            for host in CmkObject.hostnames:
                current_time = int(time.time())
                end_time = current_time+28800
                duration = 28800
                #SCHEDULE_HOST_DOWNTIME;<host_name>;<start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>
                msg = "COMMAND [%s] SCHEDULE_HOST_DOWNTIME;%s;%s;%s;1;0;%s;automation;%s\n" %\
                    (current_time, host, current_time, end_time, duration, CmkObject.message)
                cmd_list.append(msg)

                #SCHEDULE_HOST_SVC_DOWNTIME;<host_name>;<start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>
                msg = "COMMAND [%s] SCHEDULE_HOST_SVC_DOWNTIME;%s;%s;%s;1;0;%s;automation;%s\n" %\
                    (current_time, host, current_time, end_time, duration, CmkObject.message)
                cmd_list.append(msg)
            config.logger.debug("CMK set downtime message: %s", cmd_list)

        if action == 'enable':
            config.logger.info("Enabling notifications for host(s):%s",\
                CmkObject.hostnames)
            for host in CmkObject.hostnames:
                current_time = int(time.time())
                msg = "COMMAND [%s] DEL_DOWNTIME_BY_HOST_NAME;%s\n" %\
                    (current_time, host)
                cmd_list.append(msg)
            config.logger.debug("CMK remove downtime message: %s", cmd_list)
        client_socket=send_cmk_cmds(CmkObject, cmd_list)

        #Check to see if livestatus returned anything from the above this also
        #will close the socket, nothing is expected to be returned.
        msg=read_livestatus_result(client_socket)
        if msg:
            #Nothing should be returned from above call
            config.logger.info("unexpected message recieved from set_notification_state:%s", msg)


def read_livestatus_result(client_socket, timeout=2):
    '''Reads a livestatus result from the cmk server, returns msg which
    has the output from the read, CMK requires blocking sockets'''
    config.logger.info('reading livestatus results')
    #the livestatus socket for some reason does not return data
    #without first shutting down the Write part of the client first.
    #no further writes are possible after this, so the socket is 
    #closed afterwards
    client_socket.shutdown(socket.SHUT_WR)

    #TODO: CLEAN THESE COMMENTS UP.. NOW OBSOLETE
    #make socket non blocking
    #this no longer seems to be an issue now that we are specifically opening
    #and closing a socket for the communications.
    #client_socket.setblocking(0)

    #total data partwise in an array
    total_data = []
    data = ''

    #beginning time
    begin = time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = client_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except socket.error, (value, message):
            config.logger.warn("socket error %s: %s", value, message)

    #join all parts to make final string
    msg = ''.join(total_data)
    if msg:
        config.logger.debug("live status message:%s", msg)
    else:
        config.logger.debug("empty message returned from livestatus")
    clean_sock(client_socket)
    return msg

def check_status(cmk_object):
    '''Used to check the current monitoring status of a host.
    further documentaion on livestatus and the lql format
    can be found at:
    https://mathias-kettner.de/checkmk_livestatus.html
    http://www.aboutmonitoring.com/mk-livestatus-accessing-nagios-data-unixcat-lql/
    if a result is returned, there is some issue'''

    lql_file = 'lql/verify_before_patch.lql'
    lql_data = open(lql_file).read()
    cmd_list = []
    config.logger.info("Checking status of host(s).. %s ",\
        cmk_object.hostnames)
    lql = lql_data % '|'.join(cmk_object.hostnames)
    cmd_list.append(lql)
    client_socket = send_cmk_cmds(cmk_object, cmd_list)
    result = read_livestatus_result(client_socket)
    return result

def cmk_get_hosts(cmk_object):
    '''Used to get a list of hosts from the monitoring server'''
    lql_file = 'lql/get_hosts.lql'
    lql_data = open(lql_file).read()
    cmd_list = []
    cmd_list.append(lql_data)
    client_socket = send_cmk_cmds(cmk_object, cmd_list)
    result = read_livestatus_result(client_socket)
    return result


def main():
    module = AnsibleModule(
        argument_spec = dict(
            cmk_server           = dict(required=True, type='str'),
            cmk_port             = dict(required=False, default='6557', type='int'),
            hostnames            = dict(required=True, type='str'),
            action               = dict(required=True, Type='str'),
            reason               = dict(required=True, Type='str'),
    ),
        supports_check_mode=False,
    )
    cmk_server = module.params['cmk_server']
    cmk_port = module.params['cmk_port']
    hostnames = module.params['hostnames']
    action = module.params['action']
    reason = module.params['reason']

    cmk_obj = CmkObject(cmk_server,cmk_port, hostnames,reason)
    set_notification_state(cmk_obj, action)
    module.exit_json(changed=True)
if __name__ == "__main__":
    main()

