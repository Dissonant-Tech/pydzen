import os
import re
import subprocess
import time

from pydzen import config
from plugin import Plugin, Mode, Position


class WlanPlugin(Plugin):
    """Shows Date and Time"""
    def __init__(self):
        super(WlanPlugin, self).__init__()
        self._position = Position.right
        self._timeout = 4
        self._interface = 'wlp3s0'
        self._icon_wifi = ''

    def update(self, queue):
        while True:
            try:

                IWCONF = str(subprocess.check_output(['iwconfig', self._interface])).split('\\n')
                ESSID = re.findall('"([^"]*)"', IWCONF[0])

                if not ESSID:
                    LINKPERC = 0
                    ESSID = 'N/A'
                else:
                    ESSID = ESSID[0]
                    LQ = IWCONF[5].split('/')
                    LINKCUR = LQ[0][-2:]
                    LINKMAX = LQ[1][:2]
                    LINKPERC = (int(LINKCUR)*100/int(LINKMAX))

                if LINKPERC < 20:
                    self._icon_wifi = 'wireless1.xbm'
                elif LINKPERC < 40:
                    self._icon_wifi = 'wireless2.xbm'
                elif LINKPERC < 60:
                    self._icon_wifi = 'wireless3.xbm'
                elif LINKPERC < 80:
                    self._icon_wifi = 'wireless4.xbm'
                else:
                    self._icon_wifi = 'wireless5.xbm'

                queue.put({ self.__class__.__name__: (self.insertIcon(self._icon_wifi)+" "+ESSID)})
            except Exception as e:
                self._logger.debug(e)

            time.sleep(self._timeout)
