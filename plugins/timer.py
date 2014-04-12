#
# Copyright (C) 2008 Rico Schiekel (fire at downgra dot de)
#
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

import time
import datetime
import logging
import os

from pydzen import config, utils

logger = logging.getLogger('plugins.timer')

ICON = os.path.join(config.ICON_PATH, 'clock.xbm')
TIMEOUT = 2

def format_td(seconds):
    td = datetime.timedelta(seconds = seconds)
    sec = td.days * 24 * 60 * 60 + td.seconds
    min, sec = divmod(sec, 60)
    hrs, min = divmod(min, 60)
    return '%02d:%02d:%02d' % (hrs, min, sec)

def update(queue):
    while True:
        try:
            queue.put({ 'plugins.timer': ('^fg()^i('+ICON+')^fg() '+str(time.strftime('%b, %d  %H:%M')))})
        except Exception as e:
            logger.warn(e)
        
        time.sleep(TIMEOUT)
