#!/bin/sh

alignment=$1
title=$2

screenWidth=$(sres -W)
panelWidth=$(($screenWidth/3))
panelHeight=20
xpos=0

font="terminess:pixelsize=9,-*-tewi-medium-*-normal-*-11-*-*-*-*-*-*-*"

if [[ "$alignment" = "c" ]]; then

    # Move panel to center of screen
    xpos=$panelWidth

elif [[ "$alignment" = "r" ]]; then
    
    # Move panel to the right, add 1 pixel to width
    xpos=$(($panelWidth*2))
    panelWidth=$(($panelWidth+1))
fi

dzen2 -p -e 'button2=;' -h $panelHeight -dock -ta $alignment -title-name $title -fn "$font" -dock -fg "#B0B0B0" -bg "#242424" -w $panelWidth -x $xpos
