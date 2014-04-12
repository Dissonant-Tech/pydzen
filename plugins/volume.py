# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# vim:syntax=python:sw=4:ts=4:expandtab

import os
import logging
import subprocess
import re
import time

TIMEOUT = 3

from pydzen import config, utils


ICON_VOL = config.ICON_PATH+'volume0.xbm'
logger = logging.getLogger('plugins.volume')


def update(queue):
    while True:
        try:
            HEADPHONE = str(subprocess.check_output(['amixer', '-c', '0', 'contents',
                                                '|', 'grep', '17']))

            VOL = str(subprocess.check_output(['amixer', 'get', 'Master']))
            VOL = re.findall(r'\[(.+?)\]',VOL)

            if VOL[2] == 'off':
                ICON_VOL = config.ICON_PATH+'vol3.xbm'
            elif 'values=on' in HEADPHONE:
                ICON_VOL = config.ICON_PATH+'headphone1.xbm'
            else:
                if int(VOL[0].strip('%')) >= 40:
                    ICON_VOL = config.ICON_PATH+'vol1.xbm'
                elif int(VOL[0].strip('%')) > 0:
                    ICON_VOL = config.ICON_PATH+'vol2.xbm'
                else:
                    ICON_VOL = config.ICON_PATH+'vol3.xbm'

            queue.put({'plugins.volume': '^i(%s) %s' % (ICON_VOL, VOL[0])})

            time.sleep(TIMEOUT)

        except Exception as e:
            logger.warn(e)
