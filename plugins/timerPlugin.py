import os, time, datetime

from pydzen import config
from plugin import Plugin, Mode, Position


class TimerPlugin(Plugin):
    """Shows Date and Time"""
    def __init__(self):
        super(TimerPlugin, self).__init__()
        self._position = Position.right
        self._timeout = 2
        self._icon = self.insertIcon('clock.xbm')

    def update(self, queue):
        icon_out = self.setBgColor(self.pad(self._icon, 2), self._bg_light)
        while True:
            try:
                queue.put({ self.__class__.__name__: (icon_out + str(time.strftime(' %b, %d  %H:%M ')))})
            except Exception as e:
                self._logger.debug(e)

            time.sleep(self._timeout)

