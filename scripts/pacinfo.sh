#!/bin/bash

SLEEP=1

# Font
FONT="-artwiz-cure-medium-r-normal-*-10-*-*-*-*-*-*-*"

# Colors
BG="#151515"
FG="#303030"

RED="#E84F4F"

GREEN="#B8D68C"

YELLOW="#E1AA5D"

BLUE="#7DC1CF"

MAGENTA="#9B64FB"

CYAN="#0088CC"

# Geometry
HEIGHT=20
WIDTH=20
X=3
Y=48

while :; do

echo "^fg($RED) CORE ^fg($CYAN)^pa(100)$(grep core $PYDZEN_DIR/scripts/pacupdates | wc -l) 
^fg($RED) COMMUNITY ^fg($CYAN)^pa(100)$(grep community $PYDZEN_DIR/scripts/pacupdates | wc -l) 
^fg($RED) EXTRA ^fg($CYAN)^pa(100)$(grep extra $PYDZEN_DIR/scripts/pacupdates | wc -l) ^pa(117)
^fg($RED) TESTING ^fg($CYAN)^pa(100)$(grep testing $PYDZEN_DIR/scripts/pacupdates | wc -l) ^pa(117)
^fg($RED) MULTILIB ^fg($CYAN)^pa(100)$(grep multilib $PYDZEN_DIR/scripts/pacupdates | wc -l) ^pa(117)"

done | dzen2 -p -bg $BG -fg $YELLOW -y $Y -x $X -fn $FONT -l 5 -w 119 -ta l -e "button2=exit"
