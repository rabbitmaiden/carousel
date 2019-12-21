#!/bin/bash

TTY=`tty`

if [[ "$TTY" =~ /dev/pts/[0-9]* ]];
    then
        echo Hi over SSH
        exit
fi

python3 carousel.py