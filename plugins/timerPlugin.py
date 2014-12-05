import os, time, datetime

from pydzen import config
from plugin import Plugin, Mode, Position


class TimerPlugin(Plugin):
    """Shows Date and Time"""
    def __init__(self):
        super(TimerPlugin, self).__init__()
        self._position = Position.right
        self._timeout = 2
        self._icon = 'clock.xbm'

    def update(self, queue):
        while True:
            try:
                queue.put({ self.__class__.__name__: (self.insertIcon(self._icon)+str(time.strftime('%b, %d  %H:%M ')))})
            except Exception as e:
                self._logger.debug(e)

            time.sleep(self._timeout)

