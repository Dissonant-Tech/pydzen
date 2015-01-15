import subprocess

from pydzen import config
from plugin import Plugin, Mode, Position


class BspwmPlugin(Plugin):
    """Bspwm Pager plugin"""
    def __init__(self):
        super(BspwmPlugin, self).__init__()
        self._position = Position.left
        self._icon_logo = 'arch_10x10.xbm'
        # Pager Icons
        self._icon_focused = "●  "
        self._icon_used = "◎  "
        self._icon_empty = "○  "
        self._icon_urgent = "◉  "
        # Pager colors
        self._color_focused_fg = '#F1F0FF'
        self._color_focused_bg = '#242424'
        self._color_free_fg = '#6699CC'
        self._color_free_bg = '#242424'
        self._color_urgent_fg = '#F9A299'
        self._color_urgent_bg = '#34322E'
        # Pager tile icons
        self._icon_tiled = 'ntile.xbm'
        self._icon_monocole = 'monocle.xbm'

    def update(self, queue):
        try:
            # Subscribe to bspwm
            sub = subprocess.Popen(['bspc', 'control', '--subscribe'], stdout=subprocess.PIPE)

            logo_out = self.insertIcon(self._icon_logo)

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

                pager = self.parse_Pager(ws) 
                pager = self.setBgColor(self.pad(pager) , "#242424");

                output = pager + self.parse_tiling(tile)

                queue.put({self.__class__.__name__: ("  "+logo_out+"  " + output)})
        except Exception as e:
            self._logger.exception(e)
        finally:
            sub.terminate()


    def parse_Pager(self, wm):
        result = ""
        for w in wm:
            if w.startswith("O"):
                result += self.setFgColor(self.setBgColor(self.onClick("bspc desktop -f"+w[-1], self._icon_focused), self._color_focused_bg), self._color_focused_fg)
            elif w.startswith("F"):
                result += self.setFgColor(self.setBgColor(self.onClick("bspc desktop -f"+w[-1], self._icon_focused), self._color_focused_bg), self._color_focused_fg)
            elif w.startswith("U"):
                result += self.setFgColor(self.setBgColor(self.onClick("bspc desktop -f"+w[-1], self._icon_focused), self._color_focused_bg), self._color_focused_fg)
            elif w.startswith("o"):
                result += self.setFgColor(self.setBgColor(self.onClick("bspc desktop -f"+w[-1], self._icon_used), self._color_free_bg), self._color_free_fg)
            elif w.startswith("f"):
                result += self.setFgColor(self.setBgColor(self.onClick("bspc desktop -f"+w[-1], self._icon_empty), self._color_free_bg), self._color_free_fg)
            elif w.startswith("u"):
                result += self.setFgColor(self.setBgColor(self.onClick("bspc desktop -f"+w[-1], self._icon_urgent), self._color_urgent_bg), self._color_urgent_fg)

        return result

    def parse_tiling(self, tile):
        tile_type = ""
        # Desktop is tiled
        if tile.startswith("LT"):
            tile_type = self.setFgColor(self.insertIcon(self._icon_tiled), self._color_focused_fg)
        # Desktop is monocle
        elif tile.startswith("LM"):
            tile_type = self.setFgColor(self.insertIcon(self._icon_monocole), self._color_focused_fg)

        return self.pad(tile_type)
