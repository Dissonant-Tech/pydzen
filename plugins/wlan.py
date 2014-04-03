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
import re
import logging
import subprocess
import time

from pydzen import config, utils

# ------- user config ----------------------------------------------------------
INTERVAL = 1
IFACE = 'wlp3s0'
TIMEOUT = 4
# ------- user config ----------------------------------------------------------

logger = logging.getLogger('plugins.wlan')

def update(queue):
    while True:
        try:

            IWCONF = str(subprocess.check_output(['iwconfig', IFACE])).split('\\n')
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
                ICON_WIFI = 'wireless1.xbm'
            elif LINKPERC < 40:
                ICON_WIFI = 'wireless2.xbm'
            elif LINKPERC < 60:
                ICON_WIFI = 'wireless3.xbm'
            elif LINKPERC < 80:
                ICON_WIFI = 'wireless4.xbm'
            else:
                ICON_WIFI = 'wireless5.xbm'

            # lqbar = utils.gdbar('%s %s' % (lq['val'][0], lq['max'][0]), sw = 1, ss = 1, w = 15 )
            queue.put({ 'plugins.wlan': '^i(%s) %s' % (os.path.join(config.ICON_PATH, ICON_WIFI), ESSID)})
        except Exception as e:
            logger.error(e)

        time.sleep(TIMEOUT)

