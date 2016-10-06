This Repo is for UDM Ansible Initiative under UDM SIP sponsored by UDM
==============================================

SIP Summary and Background
-------------------

The purpose of this project is to produce playbooks that Unix BAU teams can use on a daily basis.
This project also aims to produce a “roadshow” for Ansible to convince Unix team to use the tools. 
To attain this, team members need to get the involvement from start. 
This will form a virtual team in which team members will be involve on creating a playbooks and own the activity themselves.



**Currently the team are working to deliver this BAU tasks**

- BAU Adhoc tasks - Joseph Tejal
- BAU Handover    - Ariel Yumul
- BAU Server Resource Management - Christian Cruz
- User/Account Management - Ian Dennison
- Patch-Management - Michael Calizo

**Other Goals:**
- To show everyone that even without Ansible formal training - BAU can still come up with fundamental solution to efficiently handle BAU tasks using the tool
- To learn how to use Git repository
- To learn how to use Ansible tower

Playbooks/roles created
-------------------

**BAU Adhoc tasks:**
- c_logs.yml 	
- c_stats.yml 	
- c_uptime.yml 	
- daily.yml 	
- r_cron.yml 	
- r_install.yml 	
- r_script.yml 	

**BAU Handover**
- bau_handover

**User-Management**
 - user_groups - the groups to add
 - user_remove - the userid to remove
 - user_add - The non-ssh Userids to add
 - user_add_ssh - The Userids with an SSH key to add
 
**Server Resource Management**

**CPU, memory and disk mangement**

Scope: Reconfigure CPU, memory and disk.
Template/playbook: cpu_memory_disk

**FILESYSTEM MANAGEMENT**

Scope: Scan/rescan of disk, creation/extensiong of volume group and creation/extension of filesystem
Template/playbook: 
cpu_memory_disk
-	Re-configure CPU, memory and disk resource
Filesystem - disk new
-	Scan for new disk
Filesystem - disk increase
-	Re-scan for disk increase
Filesystem - vg create
-	Volume group creation
Filesystem - vg extend
-	Volume group extension
Filesystem - fs new
-	Filesystem creation
Filesystem - fs increase
-	Filesystem increase
Filesystem – All
-	Scan for new disk
-	Volume group creation
-	Filesystem creation

 **Patch Management**

Forked from ACC initiative. Currently being work to test further.

ADDED TEST TEXT