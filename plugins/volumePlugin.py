import os
import subprocess
import re
import time

from pydzen import config
from plugin import Plugin, Mode, Position

class VolumePlugin(Plugin):
    """ Shows volume level"""
    def _init(self):
        super(VolumePlugin, self).__init__()
        self._timeout = 3
        self._icon = "volume0.xbm"

    def update(self, queue):
        try:
            self.updateVolume(queue)
            # if user has not set sxhkd fifo use a timer to update volume
            if os.environ.get('SXHKD_FIFO'):
                # read the sxhkd fifo
                sub = subprocess.Popen(['cat', os.environ.get('SXHKD_FIFO')], stdout=subprocess.PIPE)
                while True:
                    line = sub.stdout.readline().decode()
                    if line.startswith('HXF86Audio'):
                        self.updateVolume(queue)
            else:
                self.updateVolume(queue)
                time.sleep(self._timeout)
        except Exception as e:
            self._logger.exception(e)
        finally:
            sub.terminate()

    def updateVolume(self, queue):
        AMIXER = subprocess.Popen(['amixer', '-c', '0', 'contents'], stdout = subprocess.PIPE)
        HEADPHONE = subprocess.Popen(['grep', '17','-A', '2'], stdin=AMIXER.stdout, stdout = subprocess.PIPE)
        AMIXER.stdout.close()

        VOL = str(subprocess.check_output(['amixer', 'get', 'Master']))
        VOL = re.findall(r'\[(.+?)\]',VOL)
        VOL[0] = VOL[0].strip('%')

        # Is the sound muted?
        if VOL[2] == 'off':
            ICON_VOL = config.ICON_PATH+'vol3.xbm'
        elif 'values=on' in HEADPHONE.communicate()[0].decode():
            ICON_VOL = config.ICON_PATH+'headphone1.xbm'
        else:
            if int(VOL[0]) >= 40:
                ICON_VOL = config.ICON_PATH+'vol1.xbm'
            elif int(VOL[0]) > 0:
                ICON_VOL = config.ICON_PATH+'vol2.xbm'
            else:
                ICON_VOL = config.ICON_PATH+'vol3.xbm'

        HEADPHONE.stdout.close()

        icon_out = self.setBgColor(self.pad(self.insertIcon(ICON_VOL), 2), "#242424")
        output = icon_out + self.pad(VOL[0])

        queue.put({self.__class__.__name__: output})
