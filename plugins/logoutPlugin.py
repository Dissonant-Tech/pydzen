
from pydzen import config
from plugin import Plugin, Mode, Position

class LogoutPlugin(Plugin):
    """Power/Logout button"""
    def __init__(self):
        super(LogoutPlugin, self).__init__()
        self._icon = self.insertIcon('logout1.xbm')
        self._color = "#870000"

    def update(self, queue):
        output = self.pad(self.setFgColor(self._icon, self._color), 2)
        output = self.onClick('logout_menu/popup_menu', output)
        queue.put({self.__class__.__name__: output})
