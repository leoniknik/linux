#!/bin/bash
DIR1='/tmp/files'
DIR2='/tmp/files/history'
if [ ! -d "$DIR1" ]; then
    # Создать папку, только если ее не было
    mkdir $DIR1
    mkdir $DIR2
fi
dt=`date +%Y%H%M%S`
mv /tmp/files/actual /tmp/files/history/$dt
io=`echo iostat -px`
$io > /tmp/files/actual
cat /proc/net/dev >> /tmp/files/actual
dfd=`echo df -ah`
dfi=`echo df -ahi`
echo >> /tmp/files/actual
$dfd >> /tmp/files/actual
echo >> /tmp/files/actual
$dfi >> /tmp/files/actual
echo >> /tmp/files/actual
nt=`echo netstat -ant`
$nt >> /tmp/files/actual
echo >> /tmp/files/actual
cat /proc/net/tcp >> /tmp/files/actual
echo >> /tmp/files/actual
cat /proc/net/udp >> /tmp/files/actual
echo >> /tmp/files/actual

