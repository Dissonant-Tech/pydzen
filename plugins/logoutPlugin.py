
from pydzen import config
from plugin import Plugin, Mode, Position

class LogoutPlugin(Plugin):
    """Power/Logout button"""
    def __init__(self):
        super(LogoutPlugin, self).__init__()
        self._icon = self.insertIcon('logout1.xbm')
        self._color = "#FF0000"

    def update(self, queue):
        output = self.setFgColor(self._icon, self._color)
        queue.put({self.__class__.__name__: output})
