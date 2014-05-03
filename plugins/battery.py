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

import os
import re
from log.centrallogger import Logger
import math
import time

from pydzen import config, utils

logger = Logger(config.LOG_QUEUE)

# ------- user config ----------------------------------------------------------
BAT = '/sys/class/power_supply/BAT1'
AC = '/sys/class/power_supply/ACAD'

ICON_BAT = os.path.join(config.ICON_PATH, 'bat_full_01.xbm')
ICON_AC = os.path.join(config.ICON_PATH, 'ac15.xbm')
# ------- user config ----------------------------------------------------------

RE_FULL_CAPACITY = re.compile(r'^last full capacity:\s+(?P<lastfull>\d+).*$')
RE_REMAINING_CAPACITY = re.compile(r'^remaining capacity:\s+(?P<remain>\d+).*$')
RE_PRESENT_RATE = re.compile(r'^present rate:\s+(?P<rate>\d+).*$')
RE_AC_ONLINE = re.compile(r'^state:\s*(?P<state>on.line).*$')

def update(queue):
    try:
        while True:
            fg_color = config.FG_COLOR
            icon = os.path.join(config.ICON_PATH, 'bat_full_01.xbm')

            ac_vals = bool(int(open(os.path.join(AC, 'online')).read()))
            #ac_vals = bool(int(open(os.path.join(AC, 'online')).read()))

            lastfull = int(open(os.path.join(BAT, 'energy_full')).read())
            remain = int(open(os.path.join(BAT, 'energy_now')).read())
            rate = int(open(os.path.join(BAT, 'voltage_now')).read())

            #lastfull = int(open(os.path.join(BAT, 'charge_full')).read())
            #remain = int(open(os.path.join(BAT, 'charge_now')).read())
            #rate = int(open(os.path.join(BAT, 'voltage_now')).read())

            percent = int(100 / lastfull * remain)
            if percent < 25:
                fg_color = config.FG_COLOR_URGENT
                icon = os.path.join(config.ICON_PATH, 'bat_empty_01.xbm')
                fg_color = '#FF3300'
            elif percent < 50:
                fg_color = config.FG_COLOR_NOTICE
                icon = os.path.join(config.ICON_PATH, 'bat_low_01.xbm')
                fg_color = ' '

            bat = utils.gdbar('%s %s' % (remain, lastfull), l = '%d%% ' % percent)

            ac = ''
            if ac_vals:
                mins = (3600.0 * (float(remain) / float(rate))) / 60.0
                hours = math.floor(mins / 60.0)
                mins = math.floor(mins - (hours * 60.0))
                ac = ' %02d:%02d' % (hours, mins)
                icon = ICON_AC
                fg_color = '#FFFFFF'

            queue.put({ 'plugins.battery': '^fg(%s)^i(%s)^fg() %s' % (fg_color, icon, percent)})

            time.sleep(4)
    except Exception as e:
        logger.exception(e)
