#!/usr/bin/env python
'''This module contains functions used for talking with check_MK livestatus
Can set downtime, remove downtime, and check for any critial errors'''
# Nagios downtime and status checks, using livestatus
# This module also handles logging functions for the main project.

# AUTHOR: Steve Foris (steve.foris@datacom.co.nz)
# DATE: 2015/10/19

#TODO - make another call to livestatus to check  downtime flag has been properly set.

#python modules
import sys
import argparse
import socket
import time
verbose = False

#project modules
import config

#The class below could just be defined as a dict, using a class to add further
#capability in the future if required.
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

def set_notification_state(CmkObject, notify):
    '''Takes a cmk_object and notification state (True / False) as arguments
    if set to True notification is enabled'''
    
    if config.dryrun:
        config.logger.info('running in drymode, no change to monitoring state')
    else:
        #This function is used to set or remove downtime for specified hosts.
        cmd_list = []
        if notify == False:
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

        if notify == True:
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


def get_args():
    '''Uses the parser module to determine what arguements are passed on the
    command line'''
    parser = argparse.ArgumentParser(description='Enable or Disable nagios blackouts on a list of hostnames\n \
                                                  example: ./monitoring.py -t host1 host2 -m "patching for CO 123" -d')

    parser.add_argument('-t', '--targets',
                        action='append',
                        dest='hostnames',
                        nargs='+',
                        required=True,
                        help='A list of hosts to set notifications state')
    parser.add_argument('-m', '--message',
                        action='store',
                        dest='message',
                        help='message for a comment on the hosts for downtime')
    parser.add_argument('-e', '--enable',
                        action='store_true',
                        dest='enable_notifications',
                        default=None,
                        help='enable notifications')
    parser.add_argument('-d', '--disable',
                        action='store_false',
                        dest='enable_notifications',
                        default=None,
                        help='disable notifications')
    parser.add_argument('-s', '--server',
                        action='store',
                        dest='cmk_server',
                        default='192.168.56.52',
                        help='CMK server to connect to')
    parser.add_argument('-p', '--port',
                        action='store',
                        dest='cmk_server_port',
                        default=6557,
                        help='CMK server tcp port')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='Verbose output / Debug output')

    args = parser.parse_args()
    return args

def init():
    '''Get commanline arguments, returns all cli arguments, as well as the
    parsed results'''
    cli_args = get_args()

    #params for livestatus request
    hostnames = cli_args.hostnames[0]
    enable_notifications = cli_args.enable_notifications
    message = cli_args.message

    return cli_args, hostnames, enable_notifications, message

def main():
    '''Main section of monitoring.py'''
    cli_args, hostnames, enable_notifications, message = init()
    cmk_req = CmkObject(cli_args.cmk_server, cli_args.cmk_server_port, hostnames, message)

    #if cli_args.enable_notifications == None:
    #    print "Missing option to disable or enable notifications\
    #           see -h for help about options -d or -e "
    #    sys.exit(1)
    #else:
    #    status = check_status(cmk_req)
    #    print "status result", status
    # Commented out for not interrupting the patching process
    #    if status: 
    #        config.logger.error("Critical state detected on target host(s), not changing notification state")
    #    else:
    set_notification_state(cmk_req, enable_notifications)

if __name__ == "__main__":
    main()
