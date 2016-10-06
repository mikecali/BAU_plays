# from __future__ import (absolute_import, division, print_function)
# __metaclass__ = type
DEVICE_PREFIXES = {
 'vmware-paravirtual': 'sd',
 'xen': 'xvd',
 'kvm': 'vd',
 'other': 'vd'
}

DISK_PREFIXES = {
 1: 'a',
 2: 'b',
 3: 'c',
 4: 'd',
 5: 'e',
 6: 'f',
 7: 'g',
 8: 'h',
 9: 'i',
 10: 'j',
 11: 'k',
 12: 'l',
 13: 'm',
 14: 'n',
}

def device_num(num):
    return DISK_PREFIXES[num]

def device_prefix(prefix):
    return DEVICE_PREFIXES[prefix]

class FilterModule(object):

    def filters(self):
        return {
            'device_num' : device_num,
            'device_prefix' : device_prefix
        }

