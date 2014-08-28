import os
import sys
from log.centrallogger import Logger
import traceback
import subprocess

from pydzen import config, utils


logger = Logger(config.LOG_QUEUE)

###### COLOR OPTIONS #######
FOREGROUND='#B0B0B0'
BACKGROUND='#242424'
FOCUSED_FG='#F1F0FF'
FOCUSED_BG='#242424'
FOCUSED_OCCUPIED_FG='#F1F0FF'
FOCUSED_OCCUPIED_BG='#242424'
FOCUSED_FREE_FG='#F1F0FF'
FOCUSED_FREE_BG='#242424'
FOCUSED_URGENT_FG='#34322E'
FOCUSED_URGENT_BG='#242424'
OCCUPIED_FG='#6699CC'
OCCUPIED_BG='#242424'
FREE_FG='#6699CC'
FREE_BG='#242424'
URGENT_FG='#F9A299'
URGENT_BG='#34322E'
LAYOUT_FG='#A3A6AB'
LAYOUT_BG='#34322E'
TITLE_FG='#C3C3E5'
TITLE_BG='#242424'
STATUS_FG='#C3C3E5'
STATUS_BG='#242424'

# Pager Icons
ICO_1 = "● "
ICO_2 = "◎ "
ICO_3 = "○ "
ICO_4 = "◉ "


def parse_Pager(wm):
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

def parse_tiling(tile):
    tile_type = ""
    # Desktop is tiled
    if tile.startswith("Lt"):
        tile_type = "^fg("+FOCUSED_FG+")^bg("+FOCUSED_BG+")  ^i("+os.path.join(config.ICON_PATH, 'ntile.xbm')+")^fg()^bg()"
    # Desktop is monocle
    elif tile.startswith("Lm"):
        tile_type = "^fg("+FOCUSED_FG+")^bg("+FOCUSED_BG+")  ^i("+os.path.join(config.ICON_PATH, 'monocle.xbm')+")^fg()^bg()"

    return tile_type

def update(queue):
    try:
        # Subscribe to bspwm
        sub = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)

        # Icon is sent only once, so you must restart to change the icon
        script = os.path.join(config.SCRIPT_PATH, 'update.sh')
        queue.put({'plugins.icon': utils.onClick('1', script, '^i('+os.path.join(config.ICON_PATH, config.LOGO+')', ))})

        while True:
            line = sub.stdout.readline()
            line = str(line)
            ws = line.split(":")
            # last entry in array is tiling type (tiled/monocle)
            tile = ws[-1]
            # the first and last entries dont pertain to
            # the pager/workspaces
            ws.remove(ws[0])
            ws.remove(ws[-1])

            pager = parse_Pager(ws) + parse_tiling(tile)
            queue.put({'plugins.pager': pager})
    except Exception as e:
        logger.exception(e)
    finally:
        sub.terminate()
