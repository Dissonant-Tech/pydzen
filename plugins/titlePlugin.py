import os
import sys
import subprocess

from pydzen import config
from plugin import Plugin, Mode, Position

class TitlePlugin(Plugin):
    """Prints title of current window"""
    def __init__(self):
        super(TitlePlugin, self).__init__()

    def update(self, queue):
        try:
            sub = subprocess.Popen(['xtitle', '-s'], stdout=subprocess.PIPE)
            while True:
                line = sub.stdout.readline()
                
                # FIXME for some reason decoding the bytes makes line = None
                # but straight conversion to string leaves b'title...\n'
                line = str(line)
                line = line[2:-3]

                title = (line[:45]+'...') if len(line) > 45 else line
                queue.put({self.__class__.__name__: title})
        except Exception as e:
            self._logger.exception(e)
