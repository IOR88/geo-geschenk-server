#!/usr/bin/env bash

SUPERVISORCLS=($(pidof supervisorctl))

for i in "${SUPERVISORCLS[@]}"
do
    echo $i
    if [ $i ];then
        exec sudo kill -9 $i
    fi
done
#ERROR0=$(sudo supervisord -c /etc/supervisor/supervisord.conf  2>&1)
#
#if [ "$ERROR0" ];then
#    exec sudo pkill supervisord
#    exec sudo supervisord -c /etc/supervisor/supervisord.conf
#    echo restarted supervisord
#fi
#
#ERROR1=$(sudo supervisord -c /etc/supervisor/supervisord.conf  2>&1)
#
#if [ "$ERROR1" ];then
#    exec sudo pkill -9 supervisorctl
#    exec sudo supervisorctl -c /etc/supervisor/supervisord.conf
#    echo restarted supervisorctl
#fi