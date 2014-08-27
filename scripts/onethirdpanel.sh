#!/bin/sh

alignment=$1
title=$2

screenWidth=$(sres -W)
panelWidth=$(($screenWidth/3))
xpos=0

if [[ "$alignment" = "c" ]]; then

    # Move panel to center of screen
    xpos=$panelWidth

elif [[ "$alignment" = "r" ]]; then
    
    # Move panel to the right, add 1 pixel to width
    xpos=$(($panelWidth*2))
    panelWidth=$(($panelWidth+1))
fi

dzen2 -p -e 'button2=;' -h 16 -dock -ta $alignment -title-name $title -fn "termniness:pixelsize=10" -fg "#B0B0B0" -bg "#242424" -w $panelWidth -x $xpos
