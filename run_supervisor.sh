#!/bin/bash

# Refreshing supervisor

ERROR0=$(sudo supervisord -c /etc/supervisor/supervisord.conf  2>&1)

if [ "$ERROR0" ];then
    sudo pkill supervisord
    sudo supervisord -c /etc/supervisor/supervisord.conf
    echo restarted supervisord
fi

ERROR1=$(sudo supervisord -c /etc/supervisor/supervisord.conf  2>&1)

if [ "$ERROR1" ];then
     sudo pkill supervisorctl
     sudo supervisorctl -c /etc/supervisor/supervisord.conf
     echo restarted supervisorctl
fi

##!/bin/bash
#
#SUPERVISORCLS=($(pidof supervisorctl))
#
#for i in "${SUPERVISORCLS[@]}"
#    do
#        echo $i
#        if [ $i ];then
#            sudo kill -9 ${i}
#        fi
#    done