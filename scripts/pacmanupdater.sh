#! /bin/bash

if [[ -f $PYDZEN_DIR/scripts/pacupdates ]]; then
    rm $PYDZEN_DIR/scripts/pacupdates
fi

pacman -Sup >> $PYDZEN_DIR/scripts/pacupdates
