README - Userid and SSH Key Management
============================

The primary playbook is the **"playbook/user_management_ssh.yml"** file, which performs the following steps....
 - Adds SSH Keys for users on a jumphost (all hosts and subsets of hosts)
 - Add the Userids (SSH and Non-SSH) to all selected hosts, and remove selected hosts
 - (Optional) Add Userids (SSH and Non-SSH) to Specific subsets of hosts

User management is controlled using the **"playbooks/var_[enviromment].yml"** parameter file, which includes the following
components,....

user_groups - the groups to add
user_remove - the userid to remove
user_add - The non-ssh Userids to add
user_add_ssh - The Userids with an SSH key to add

**Environments**
The user playbooks allows specification of a list of Environments for the User to be present in. This is held in the "environments" value for each entry
in the user_add and user_add_ssh variables. Each environment should be present in the Inventory list, and there should be a separate line in the playbook calling
the role "user" with the specified environment.

eg. (Variables)
    user_add:
      - { name: rosie, state: present, .... environments: ["Prod", "UAT"]}

eg. (Playbook)
    - { role: user, target: UAT, when: inventory_hostname in groups.UAT }
    - { role: user, target: Prod, when: inventory_hostname in groups.Prod }

**Variables required:**
Usingjumphosts - this is a Boolean value in the main variables list that indicates whether a jumphost is to be configured. If set to "True", ssh keys will be copied
from this host to all others, allowing password-less access.

** Inventory Layout**
jumphosts - the "jumphosts" group should consist of one jumphost that is the central point from which users can move through the unix landscape.
This does not have to be the ansible Tower Server.
tower_host - this is the Inventory group for the Ansible Tower host, and indicates the central server used to house ssh keys and config files.

**Dependencies:**
The ansible Tower server should have the following directories and files
- user ssh keys - The directory /usr/local/ssh_lib on the Ansible Server (Inventory group "tower_host") will be used as a central point for distributing ssh keys. Each user will have their own subdirectory where
their ssh key from the jumphost will be found.

- ssh config file - the "$HOME/.ssh/config" file required for the jumphost will be the same for each user, and the template should be located on the Ansible server (Inventory group "tower_host") as
/usr/local/etc/template.file.{jumphost}.
- compress home script - This script is held on the Ansible Server (Inventory group "tower_host") /usr/local/etc/recycle_home_directory.sh and is copied out to /usr/local/bin on the remote Servers.
This script is run every time a user is deleted, and will copy the contents of the home directory to a zipped file and remove it.

**User role:**
The "user" role is comprised of several steps, including add groups and users. A UID can be specified as part of the Userid addition, and if no UID is specified, the OS will add
the Userid with it's own next free UID.

**Jump Hosts:** 
    This is a central Server that is used by the Admins to jump into all other hosts.
	This host is defined using the "jumphosts" inventory group and the "isjumphost" variable
	being set to true. It will hold the master ssh key for each user, which be used to 
	add to authorized_keys for each user on the client servers.
	The master variable for using jumphosts is at the top of the variables .yml file, with the
	value "usingjumphost" being set to "true". If the value is set to "false" or is undefined,
	then no jumphost related activity will take place. SSH Keys will be generated regardless
	of this setting, but will only be copied around when it is set to "true".
