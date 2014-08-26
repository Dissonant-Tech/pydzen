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
from log.centrallogger import Logger
import subprocess
import re
import time
from pydzen import config, utils


TIMEOUT = 3
ICON_VOL = config.ICON_PATH+'volume0.xbm'
logger = Logger(config.LOG_QUEUE)

def updateVOL(queue):
    AMIXER = subprocess.Popen(['amixer', '-c', '0', 'contents'], stdout = subprocess.PIPE)
    HEADPHONE = subprocess.Popen(['grep', '17','-A', '2'], stdin=AMIXER.stdout, stdout = subprocess.PIPE)
    AMIXER.stdout.close()

    VOL = str(subprocess.check_output(['amixer', 'get', 'Master']))
    VOL = re.findall(r'\[(.+?)\]',VOL)

    if VOL[2] == 'off':
        ICON_VOL = config.ICON_PATH+'vol3.xbm'
    elif 'values=on' in HEADPHONE.communicate()[0].decode():
        ICON_VOL = config.ICON_PATH+'headphone1.xbm'
    else:
        if int(VOL[0].strip('%')) >= 40:
            ICON_VOL = config.ICON_PATH+'vol1.xbm'
        elif int(VOL[0].strip('%')) > 0:
            ICON_VOL = config.ICON_PATH+'vol2.xbm'
        else:
            ICON_VOL = config.ICON_PATH+'vol3.xbm'

    HEADPHONE.stdout.close()
    queue.put({'plugins.volume': '^i(%s) %s' % (ICON_VOL, VOL[0])})

def update(queue):
    try:
        updateVOL(queue)
        # if user has not set sxhkd fifo use a timer to update volume
        if os.environ.get('SXHKD_FIFO'):
            # read the sxhkd fifo
            sub = subprocess.Popen(['cat', os.environ.get('SXHKD_FIFO')], stdout=subprocess.PIPE)
            while True:
                line = sub.stdout.readline().decode()
                if line.startswith('HXF86Audio'):
                    updateVOL(queue)
        else:
            updateVOL(queue)
            time.sleep(TIMEOUT)
    except Exception as e:
        logger.exception(e)
