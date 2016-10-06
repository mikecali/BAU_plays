# SERVER INFORMATION
* Client - Customs
* Hostname - ariel1
* Project Name: bau-hand-over
* Playbook: playbooks/bau_hand_over.yml


# TABLE OF CONTENTS
===================================================================================
1. Alert Monitoring  agent Information
   1.1 List of installed Monitoring Packages
   1.2 List of running Monitoring agent
   1.3 Monitoring agent startup config 
2. Backup agent Infomration
   2.1 List of installed Backup agent Packages
   2.2 List of running Backup agent
   2.3 Backup agent startup config
3. Patching
   3.1  Server registered on the Satellite server
4. Daily Checks
   4.1 Root alias has been setup
5. Security
   5.1 Unix Support User Accounts
   5.2 Project User account
   5.3 SSH Config check
   5.4 Root authorized_keys key check
   5.5 SELinux check
   5.6 Local Firewall rules
6. Miscellaneous
   6.1 List of installed Miscellaneous Packages
   6.2 List of running Miscellaneous agent
   6.3 Miscellaneous agent startup config 
   6.4 DNS resolution check
   
=============================================
## 1. Alert Monitoring agent Information
---------------------------------------------
### 1.1 List of installed Monitoring Packages
---------------------------------------------
- Error: Monitoring package: nrpe - not installed !!!
- Error: Monitoring package: check-mk-agent - not installed !!!
 - OK: Monitoring package: net-snmp - net-snmp-5.5-54.el6_7.1.x86_64
---------------------------------------------
### 1.2 List of running Monitoring agent
---------------------------------------------
- Error: nrpe - monitoring agent not installed !!!
- Error: check-mk - monitoring agent not installed !!!
- Error: snmpd - monitoring agent is stopped !!!
-------------------------------------------
### 1.3 Monitoring agent startup config 
--------------------------------------------
- Error: Monitoring: nrpe -  !!!
- Error: Monitoring: check-mk -  !!!
- Error: Monitoring: snmpd - 3:off !!!
=============================================
## 2. Backup agent Information
---------------------------------------------
### 2.1 List of installed Backup agent Packages
---------------------------------------------
- Error: netbackup - package not installed !!!
---------------------------------------------
### 2.2 List of running Backup agent
---------------------------------------------
- Error: netbackup - agent  not running !!!
-------------------------------------------
### 2.3 Backup agent startup config
--------------------------------------------
- Error: Monitoring: netbackup -  !!!
=============================================
## 3. Patching
---------------------------------------------
### 3.1  Server registered on the Satellite server
-------------------------------------------
- OK: Loaded plugins: changelog, product-id, rhnplugin, subscription-manager,
              : versionlock
This system is receiving updates from RHN Classic or RHN Satellite.
repo id                                       repo name                   status
nov2015-clone-2-rhel-x86_64-server-optional-6 nov2015-clone of RHEL Serve  9,092
nov2015-clone-dslwg_tools_rhel6               nov2015-clone of DSLWG Tool      1
nov2015-clone-rhel-x86_64-server-6            nov2015-clone of Red Hat En 16,183
nov2015-clone-rhel-x86_64-server-extras-6     nov2015-clone of RHEL Serve     34
nov2015-clone-rhel-x86_64-server-rh-common-6  nov2015-clone of Red Hat Co     79
nov2015-clone-rhn-tools-rhel-x86_64-server-6  nov2015-clone of RHN Tools     184
repolist: 25,573
=============================================
## 4. Daily Checks
---------------------------------------------
### 4.1 Root alias has been setup
-------------------------------------------
Check if aliases file exist /etc/aliases
- OK: File exist: /etc/aliases: ASCII English text
Root Aliases 
- Error: root alias: 
=============================================	
## 5. Security
---------------------------------------------
### 5.1 Unix Support User Accounts
-------------------------------------------
Unix users:
- OK: User exist: ariely - ariely:Datacom - Ariel Yumul
- OK: User exist: rhel - rhel:Datacom Anisble Account
- OK: User exist: user1 - user1:Datacom User1
- OK: User exist: user2 - user2:Datacom User2
- OK: User exist: user3 - user3:Datacom User3
- Error: User doesn't exist: support1 -  - should be created !!!
- Error: User doesn't exist: support2 -  - should be created !!!
-------------------------------------------
### 5.2 Project Support User Accounts
-------------------------------------------
Project users:
- Error: User: proj1 - proj1:Datacom Project User1 - user should be removed !!!
- Error: User: proj2 - proj2:Datacom Project User2 - user should be removed !!!
- Error: User: proj3 - proj3:Datacom Project User2 - user should be removed !!!
- OK: User: proj4 - no longer exist
- OK: User: proj5 - no longer exist
- OK: User: proj6 - no longer exist
-------------------------------------------
### 5.3 SSH Config check
-------------------------------------------
- OK: SSH Config -  PermitRootLogin no
-------------------------------------------
### 5.4 Root authorized_keys key check
-------------------------------------------
- Error: root authorized_keys exist /root/.ssh/authorized_keys: ASCII text !!!
-------------------------------------------
### 5.5 SELinux check
-------------------------------------------
- OK: SELinux -  Enforcing
-------------------------------------------
### 5.6 Local Firewall rules
-------------------------------------------
- Error: IPTables Table: filter
Chain INPUT (policy ACCEPT)
num  target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
num  target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
num  target     prot opt source               destination          !!!
=============================================
## 6. Miscellaneous Information
---------------------------------------------
### 6.1 List of installed Miscellaneous Packages
---------------------------------------------
 - OK: Miscellaneous package: cronie - cronie-1.4.4-15.el6.x86_64
 - OK: Miscellaneous package: net-snmp - net-snmp-5.5-54.el6_7.1.x86_64
 - OK: Miscellaneous package: ntp - ntp-4.2.6p5-5.el6.x86_64
 - OK: Miscellaneous package: iptables - iptables-1.4.7-16.el6.x86_64
 - OK: Miscellaneous package: rsyslog - rsyslog-5.8.10-10.el6_6.x86_64
 - OK: Miscellaneous package: selinux-policy - selinux-policy-3.7.19-279.el6.noarch
 - OK: Miscellaneous package: postfix - postfix-2.6.6-6.el6_5.x86_64
 - OK: Miscellaneous package: audit - audit-2.3.7-5.el6.x86_64
 - OK: Miscellaneous package: mailx - mailx-12.4-8.el6_6.x86_64
---------------------------------------------
### 6.2 List of running Miscellaneous agent
---------------------------------------------
- OK: Miscellaneous agent: crond -  crond (pid  2000) is running...
- Error: snmpd - miscellaneous agent is stopped !!!
- OK: Miscellaneous agent: ntpd -  ntpd (pid  4888) is running...
- Error: iptables - miscellanous agent not installed !!!
- OK: Miscellaneous agent: rsyslog -  rsyslogd (pid  1683) is running...
- Error: sestatus - miscellanous agent not installed !!!
- OK: Miscellaneous agent: postfix -  master (pid  1986) is running...
- OK: Miscellaneous agent: auditd -  auditd (pid  1661) is running...
-------------------------------------------
### 6.3 Miscellaneous agent startup config 
--------------------------------------------
- OK: Miscellaneous agent crond - 3:on
- Error: Miscellaneous: snmpd - 3:off !!!
- OK: Miscellaneous agent ntpd - 3:on
3:off
- OK: Miscellaneous agent iptables - 3:on
- OK: Miscellaneous agent rsyslog - 3:on
- OK: Miscellaneous agent postfix - 3:on
- OK: Miscellaneous agent auditd - 3:on
-------------------------------------------
### 6.4 DNS resolution check
--------------------------------------------
- OK: DNS resolution check - www.hau.edu.ph - Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
www.hau.edu.ph	canonical name = hau.edu.ph.
Name:	hau.edu.ph
Address: 202.69.186.177
- OK: DNS resolution check - www.stuff.co.nz - Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
www.stuff.co.nz	canonical name = kona6.fairfaxmedia.com.au.edgekey.net.
kona6.fairfaxmedia.com.au.edgekey.net	canonical name = e1365.dsce2.akamaiedge.net.
Name:	e1365.dsce2.akamaiedge.net
Address: 23.43.147.119
- Error: DNS resolution check: www.arielx.co.nz - Server:		8.8.8.8
Address:	8.8.8.8#53

** server can't find www.arielx.co.nz: NXDOMAIN !!!
------------------------------------------------------------------------------------

####################################################################################

------------------------------------------------------------------------------------
* * *    Error Report Summary         * * * 
-------------------------------------------
* 1. Alert Monitoring agent Information
-------------------------------------------
** 1.1 Monitoring package not installed
-------------------------------------------
- Error: Monitoring: nrpe - package nrpe is not installed !!!
- Error: Monitoring: check-mk-agent - package check-mk-agent is not installed !!!
-------------------------------------------
** 1.2 Status of monitoring agent
--------------------------------------------
- Error: Monitoring agent: nrpe - not running !!!
- Error: Monitoring agent: check-mk - not running !!!
-------------------------------------------
** 1.3 Monitoring agent startup config 
--------------------------------------------
- Error: Monitoring: nrpe -  !!!
- Error: Monitoring: check-mk -  !!!
- Error: Monitoring: snmpd - 3:off !!!
--------------------------------------------
* 2. Backup agent Information
-------------------------------------------
** 2.1 Backup package not installed
-------------------------------------------
- Error: Backup: netbackup - package netbackup is not installed !!!
-------------------------------------------
** 2.2 Backup agent not found in the process list
--------------------------------------------
- Error: Backup agent: netbackup - not running !!!
-------------------------------------------
** 2.3  Backup agent startup config
--------------------------------------------
- Error: Backup: netbackup -  !!!
-------------------------------------------
* 3. Patching
-------------------------------------------
** 3.1  Server registered on the Satellite server
-------------------------------------------

-------------------------------------------
* 4. Daily Checks
-------------------------------------------
Root Aliases 
- Error: root alias not set !!!

-------------------------------------------
* 5. Security
-------------------------------------------
* 5.1.Unix Support User Accounts
- Error: User - support1 doesn't exist should be created!!!
- Error: User - support2 doesn't exist should be created!!!
-------------------------------------------
* 5.2 Unix Project User Accounts
-------------------------------------------
- Error: User: proj1 - proj1:Datacom Project User1 exist should be remove !!!
- Error: User: proj2 - proj2:Datacom Project User2 exist should be remove !!!
- Error: User: proj3 - proj3:Datacom Project User2 exist should be remove !!!
-------------------------------------------
* 5.3 SSH Config check
-------------------------------------------
-------------------------------------------
* 5.4 Root authorized_keys key check
-------------------------------------------
- Error: root authorized key exist -  /root/.ssh/authorized_keys: ASCII text
-------------------------------------------
* 5.5 SELinux check
-------------------------------------------
-------------------------------------------
* 5.6 Local Firewall rules
-------------------------------------------
- Error: IPTables Table: filter
Chain INPUT (policy ACCEPT)
num  target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
num  target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
num  target     prot opt source               destination          !!!
-------------------------------------------
* 6. Miscellaneous Information
--------------------------------------------
** 6.1 System Daemons
-------------------------------------------
** 6.1 List of installed Miscellaneous Packages
-------------------------------------------
-------------------------------------------
** 6.2 List of running Miscellaneous agent
--------------------------------------------
- Error: Miscellaneous agent: sestatus - not running !!!
-------------------------------------------
** 6.3 Miscellaneous agent startup config 
--------------------------------------------
- Error: Miscellaneous: snmpd - 3:off !!!
-------------------------------------------
### 6.4 DNS resolution check
--------------------------------------------
--------------------------------------------
=============================================