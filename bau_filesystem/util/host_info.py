#!/usr/bin/python
import sys
import json
import socket
import fcntl
import struct
import getpass

import requests
from requests.auth import HTTPBasicAuth

host_name = socket.gethostname()
host_description = host_name +' host'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

host_ip = get_ip_address('eth0')
host_user =  getpass.getuser()
host_variables = '{ansible_ssh_host: %s,ansible_ssh_user: %s}' % (host_ip, host_user)

host_enabled = True
host_last_job = None
host_last_job_host_summary = None

host_data = {
  'name': host_name,
  'description': host_description,
  'inventory': 1,
  'enabled': host_enabled,
  'instance_id': '',
  'variables': host_variables,
  'last_job': host_last_job,
  'last_job_host_summary': host_last_job_host_summary
}



if len(sys.argv) > 1 and sys.argv[1] == '--list':
  print json.dumps(host_data)

if len(sys.argv) > 1 and sys.argv[1] == '--upload':
  url = 'https://tower.env.care/api/v1/hosts/'
  json_formated_host_data = json.dumps(host_data)
  headers = {'content-type': 'application/json'}
  auth = HTTPBasicAuth('username', 'password')
  r = requests.post(url, data=json_formated_host_data, headers=headers, verify=False, auth=auth)

  if r.status_code >= 500:
    print 'The %s sent back a server error. Please try again later.' % (url)

  if r.status_code >= 400:
    print 'The Tower server claims it was sent a bad request. Response: %s' %(r.content.decode('utf8'))

  if r.status_code == 401:
    print 'Invalid %s authentication credentials.' % (url)
  elif r.status_code == 403:
    print 'No have permission to do this.'
  elif  r.status_code == 404:
    print 'The requested object could not be found.'
  elif  r.status_code == 405:
    print 'The Tower server says you can not make a request with this method to that URL (%s)' % (url)
  elif  r.status_code == 201:
    print 'Host data sent to %s' % (url)
