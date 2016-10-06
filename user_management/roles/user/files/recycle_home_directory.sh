#!/bin/bash

export PARM=$*
export P1=`echo "$PARM" |awk '{print $1}'`
export DTG=`date '+%Y%m%d-%H%M'`

if [[ ! -d /home/archive ]]
then
	mkdir /home/archive
fi

# Now detect cleanup
if [[ ! -d /home/${P1} ]]
then
	# Ignore, home directory does not exists
	echo "$DTG PARM $PARM no home directory" >> /tmp/cleanup.log
	exit
fi

if [[ -f /home/archive/${P1}.tar.gz ]]
then
	# already exists, ship
	echo "$DTG PARM $PARM dump file already exists" >> /tmp/cleanup.log
	exit
fi

# Zip up and correct
tar -cvf /home/archive/${P1}.tar /home/${P1}
export RC1=$?
gzip /home/archive/${P1}.tar
export RC2=$?

if [[ "$RC1$RC2" == "00" ]]
then
	echo "Zip functioned OK"
	echo "$DTG PARM $PARM Zip functioned OK" >> /tmp/cleanup.log
	rm -rf  /home/${P1}
else
	echo "Zip failed ERROR"
	echo "$DTG PARM $PARM Zip failed ERROR" >> /tmp/cleanup.log
fi	
