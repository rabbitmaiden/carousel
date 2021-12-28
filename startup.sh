#!/bin/bash

TTY=`tty`

if [[ "$TTY" =~ /dev/pts/[0-9]* ]];
    then
        echo Hi over SSH
        exit
fi

./carousel.sh  >> /home/alice/output.log
