#!/bin/bash -e

function touchscreen {
   /usr/bin/xinput $1 'ELAN Touchscreen' 
}

case $1 in
    on)
        touchscreen enable
        ;;
    off)
        touchscreen disable
        ;;
    *)
        echo "usage ${0} [on|off]"
        exit 1
        ;;
esac
