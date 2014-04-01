import os
import sys
import logging
import subprocess

from pydzen import config, utils


logger = logging.getLogger('plugins.bspwm')

###### COLOR OPTIONS #######
FOREGROUND='#B0B0B0'
BACKGROUND='#181818'
FOCUSED_FG='#F1F0FF'
FOCUSED_BG='#181818'
FOCUSED_OCCUPIED_FG='#F1F0FF'
FOCUSED_OCCUPIED_BG='#181818'
FOCUSED_FREE_FG='#F1F0FF'
FOCUSED_FREE_BG='#181818'
FOCUSED_URGENT_FG='#34322E'
FOCUSED_URGENT_BG='#181818'
OCCUPIED_FG='#6699CC'
OCCUPIED_BG='#181818'
FREE_FG='#6699CC'
FREE_BG='#181818'
URGENT_FG='#F9A299'
URGENT_BG='#34322E'
LAYOUT_FG='#A3A6AB'
LAYOUT_BG='#34322E'
TITLE_FG='#C3C3E5'
TITLE_BG='#181818'
STATUS_FG='#C3C3E5'
STATUS_BG='#181818'

# Pager Icons
ICO = "^i("+config.ICON_PATH+"/xbm/arch_10x10.xbm)"
ICO_1 = "● "
ICO_2 = "◎ "
ICO_3 = "○ "
ICO_4 = "◉ "


def parse_Pager(self, wm):
    result = ""
    for w in wm:
        if w.startswith("O"):
            result = result+"^fg("+FOCUSED_FG+")^bg("+FOCUSED_BG+")^ca(1, bspc desktop -f"+w[-1]+")^ca(2, bspc window -d "+w[-1]+") "+ICO_1+"^ca()^fg()^bg()"
        elif w.startswith("F"):
            result = result+"^fg("+FOCUSED_FG+")^bg("+FOCUSED_BG+")^ca(1, bspc desktop -f"+w[-1]+")^ca(2, bspc window -d "+w[-1]+") "+ICO_1+"^ca()^fg()^bg()"
        elif w.startswith("U"):
            result = result+"^fg("+FOCUSED_FG+")^bg("+FOCUSED_BG+")^ca(1, bspc desktop -f"+w[-1]+")^ca(2, bspc window -d "+w[-1]+") "+ICO_1+"^ca()^fg()^bg()"
        elif w.startswith("o"):
            result = result+"^fg("+FREE_FG+")^bg("+FREE_BG+")^ca(1, bspc desktop -f"+w[-1]+")^ca(2, bspc window -d "+w[-1]+") "+ICO_2+"^ca()^fg()^bg()"
        elif w.startswith("f"):
            result = result+"^fg("+FREE_FG+")^bg("+FREE_BG+")^ca(1, bspc desktop -f"+w[-1]+")^ca(2, bspc window -d "+w[-1]+") "+ICO_3+"^ca()^fg()^bg()"
        elif w.startswith("u"):
            result = result+"^fg("+URGENT_FG+")^bg("+URGENT_BG+")^ca(1, bspc desktop -f"+w[-1]+")^ca(2, bspc window -d "+w[-1]+") "+ICO_4+"^ca()^fg()^bg()"

    return result

def update(queue):
    try:
        # Subscribe to bspwm
        #sub = subprocess.Popen(['bspc', '-s'], subprocess.PIPE)
        sub = utils.pipe(bytes('bspc', 'UTF-8'), s = True)
        queue.put({'plugins.icon': os.path.join(config.ICON_PATH, config.LOGO)})
        while True:
            line = sub.stdout.readline()

            if line.startswith('T'):
                title = line[1:]
                queue.put({'plugins.title': title})
            elif line.startswith("W"):
                ws = line.split(":")
                # the first and last entries dont pertain to
                # the pager/workspaces
                ws.remove(ws[0])
                ws.remove(ws[-1])
                pager = parse_Pager(ws)
                queue.put({'plugins.pager': pager})
    except Exception as e:
        logger.error(e)
