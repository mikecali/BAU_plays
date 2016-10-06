#!/usr/bin/python
# -*- coding: utf-8 -*-


DOCUMENTATION = '''
---


'''

EXAMPLES = '''

'''

try:
    import parted
    import _ped
    import json
    HAS_LIB=True
except:
    HAS_LIB=False

#constants come from include/parted/device.in.h of parted
PED_DEVICE_UNKNOWN      = 0
PED_DEVICE_SCSI         = 1
PED_DEVICE_DM           = 12
PED_DEVICE_VIRTBLK      = 15

# https://github.com/abbbi/snippets/blob/master/python-parted.py

#constants - digital storage
DS_KB = 1024
DS_MB = 1048576
DS_GB = 1073741824
DS_TB = 1099511627776


START_OFFSET = 2048 #http://superuser.com/questions/352572/why-does-the-partition-start-on-sector-2048-instead-of-63


def sector_size(data_size):
    digital_storage_value = int(data_size[0:-2])
    digital_storage_type = data_size[-2:]


    if digital_storage_type != 'KB' and digital_storage_type != 'MB' and digital_storage_type != 'GB' and digital_storage_type != 'TB':
        module.fail_json(msg="Invalid: Storage Type must be KB, MB, GB or TB")

    if digital_storage_type == 'KB':
       return digital_storage_value * DS_KB

    if digital_storage_type == 'MB':
        return digital_storage_value * DS_MB

    if digital_storage_type == 'GB':
        return digital_storage_value * DS_GB

    if digital_storage_type == 'TB':
        return digital_storage_value * DS_TB


def parse_sizes(data):
    sizes = []
    for partition in data:
        sizes.append({
            'sector_size': sector_size(partition['size'])
        })
    return sizes



def total_size_of_sectors(data):
    total_size = 0

    for partition in data:
        total_size += partition['sector_size']

    return total_size


# def find_mapper_device_name(module, dm_device):
#         dmsetup_cmd = module.get_bin_path('dmsetup', True)
#         mapper_prefix = '/dev/mapper/'
#         rc, dm_name, err = module.run_command("%s info -C --noheadings -o name %s" % (dmsetup_cmd, dm_device))
#         if rc != 0:
#             module.fail_json(msg="Failed executing dmsetup command.", rc=rc, err=err)
#         mapper_device = mapper_prefix + dm_name.rstrip()
#         return mapper_device

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True),
            partitions=dict(required=True),
            state=dict(choices=["absent", "present"], default='present')
        ),
        supports_check_mode=True,
    )

    name = module.params['name']
    state = module.params['state']

    partitions = parse_sizes(module.params['partitions'])

    # lst = set()

    result = {"devices":{}}
    result_dev = result["devices"]

    # get all devices on system
    # devices = parted.getAllDevices();

    disk_array={};

    device = parted.Device(name)


    # for device in devices:
    disk_array[device.path] = {};
    disk_array[device.path]['raw_type'] = device.type;

    if name == device.path:
        disk_array[device.path]['target'] = 'yes';

    if device.type == PED_DEVICE_DM:
        disk_array[device.path]['type'] = 'Device Mapper';
        module.fail_json(msg="Invalid: Device is a Device Mapper.")

    if device.type == PED_DEVICE_VIRTBLK:
        disk_array[device.path]['type'] = 'Virtual Block';
        
        try:
            # see if disk is already labelled, or just raw
            disk = parted.Disk(device)

            disk_array[device.path]['sizeMB'] = device.getSize(unit='MB')
            disk_array[device.path]['length'] = device.length

            module.exit_json(changed=False, disk_array=disk_array, msg="Already partitioned")
        

        except _ped.DiskLabelException:
            disk_array[device.path]['label'] = False
            disk = parted.freshDisk(device, 'msdos')
            sector_size = device.sectorSize

            total_size = total_size_of_sectors(partitions)

          #  print("Total Size Of sectors needed: " + str(total_size))
            print ("max partition length: " + str(disk.maxPartitionLength))
            print ("max partition start sector: " + str(disk.maxPartitionStartSector))
            print ("Free Space Regions: " + str(disk.getFreeSpaceRegions))
            print ("Free Space Partitions: " + str(disk.getFreeSpacePartitions))

            start_sector =  START_OFFSET #start at 2048

            for partition in partitions:

                # get length of partition based on sector size
                length = (partition['sector_size'] // device.sectorSize) # // is a floor division operator
                end_sector = start_sector + length - 1
                geometry = parted.Geometry(device=device, start=start_sector, end=end_sector)
                partition = parted.Partition(disk=disk, type=parted.PARTITION_NORMAL, geometry=geometry)
                partition.setFlag(parted.PARTITION_LVM)
                #partition = parted.Partition(disk=disk, type=parted.PARTITION_LVM, geometry=geometry)
                disk.addPartition(partition=partition, constraint=device.optimalAlignedConstraint)
                disk.commit()

                #assign new start sector for next partition
                start_sector = end_sector

            
            module.exit_json(changed=True, disk_array=disk_array, msg="Partitions created")
    # changed=True
    # if changed:
    #     module.exit_json(changed=changed, disk_array=disk_array)
    # else:
    #     module.fail_json(msg="No physical volumes given.")

# import module snippets
from ansible.module_utils.basic import *
main()
