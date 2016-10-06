#!/bin/bash

CONFIG_FILE=/etc/sysconfig/network-scripts/ifcfg-eth0
DATE=`date`
DATESTAMP=`date +%Y-%m-%d-%H%M`
echo "Reconfigure Running at $DATE" 

TMP_FILE=reconfigure-$DATESTAMP

echo "Writing to temp file at $TMP_FILE" 
cp $CONFIG_FILE $TMP_FILE

if [ ! -z "$RECONFIGURE_BOOTPROTO" ]; then
  echo "Reconfiguring BOOTPROTO to $RECONFIGURE_BOOTPROTO"
  if grep -lq "^BOOTPROTO=" $TMP_FILE; then
    echo "Updating BOOTPROTO in place"
    sed -i "s/BOOTPROTO=.*/BOOTPROTO=$RECONFIGURE_BOOTPROTO/"       $TMP_FILE
  else
    echo "Adding BOOTPROTO"
    echo "BOOTPROTO=$RECONFIGURE_BOOTPROTO" >> $TMP_FILE
  fi
fi
if [ ! -z "$RECONFIGURE_IPADDR" ]; then
  echo "Reconfiguring IPADDR to $RECONFIGURE_IPADDR"
  if grep -lq "^IPADDR=" $TMP_FILE; then
    echo "Updating IPADDR in place"
    sed -i "s/IPADDR=.*/IPADDR=$RECONFIGURE_IPADDR/"         $TMP_FILE
  else
    echo "Adding IPADDR"
    echo "IPADDR=$RECONFIGURE_IPADDR" >> $TMP_FILE
  fi
fi  
if [ ! -z "$RECONFIGURE_GW" ]; then
  echo "Reconfiguring GATEWAY to $RECONFIGURE_GW"
  if grep -lq "^GATEWAY=" $TMP_FILE; then
    echo "Updating GATEWAY in place"
    sed -i "s/GATEWAY=.*/GATEWAY=$RECONFIGURE_GW/"   $TMP_FILE
  else
    echo "Adding GATEWAY"
    echo "GATEWAY=$RECONFIGURE_GW" >> $TMP_FILE
  fi
fi  
if [ ! -z "$RECONFIGURE_DNS1" ]; then
  echo "Reconfiguring DNS1 to $RECONFIGURE_DNS1"
  sed -i "s/DNS1=.*/DNS1=$RECONFIGURE_DNS1/"    $TMP_FILE
  if grep -lq "^DNS1=" $TMP_FILE; then
    echo "Updating DNS1 in place"
    sed -i "s/DNS1=.*/DNS1=$RECONFIGURE_DNS1/"   $TMP_FILE
  else
    echo "Adding DNS1"
    echo "DNS1=$RECONFIGURE_DNS1" >> $TMP_FILE
  fi
fi  
if [ ! -z "$RECONFIGURE_DNS2" ]; then
  echo "Reconfiguring DNS2 to $RECONFIGURE_DNS2"
  sed -i "s/DNS2=.*/DNS2=$RECONFIGURE_DNS2/"    $TMP_FILE
  if grep -lq "^DNS2=" $TMP_FILE; then
    echo "Updating DNS2 in place"
    sed -i "s/DNS2=.*/DNS2=$RECONFIGURE_DNS2/"   $TMP_FILE
  else
    echo "Adding DNS2"
    echo "DNS2=$RECONFIGURE_DNS2" >> $TMP_FILE
  fi
fi  
if [ ! -z "$RECONFIGURE_DNS3" ]; then
  echo "Reconfiguring DNS3 to $RECONFIGURE_DNS3"
  sed -i "s/DNS3=.*/DNS3=$RECONFIGURE_DNS3/"    $TMP_FILE
  if grep -lq "^DNS3=" $TMP_FILE; then
    echo "Updating DNS3 in place"
    sed -i "s/DNS3=.*/DNS3=$RECONFIGURE_DNS3/"   $TMP_FILE
  else
    echo "Adding DNS3"
    echo "DNS3=$RECONFIGURE_DNS3" >> $TMP_FILE
  fi
fi

echo "Overwriting $CONFIG_FILE with $TMP_FILE"
sudo cp $TMP_FILE $CONFIG_FILE 

if [ ! -z "$REBOOT_ON_RECONFIGURE" ]; then
  echo "Rebooting after Network Reconfigure"
  sudo reboot
fi
