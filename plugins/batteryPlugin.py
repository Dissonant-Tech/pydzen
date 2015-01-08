import os, time
import re
import math
import time

from pydzen import config
from plugin import Plugin, Mode, Position


class BatteryPlugin(Plugin):
    """Shows battery charge and staus"""
    def __init__(self):
        super(BatteryPlugin, self).__init__()
        self._position = Position.right
        self._timeout = 2
        self._bat = "/sys/class/power_supply/BAT1"
        self._ac = "/sys/class/power_supply/ACAD"
        self._re_full_capacity = re.compile(r'^last full capacity:\s+(?P<lastfull>\d+).*$')
        self._re_remaining_capacity = re.compile(r'^remaining capacity:\s+(?P<remain>\d+).*$')
        self._re_present_rate = re.compile(r'^present rate:\s+(?P<rate>\d+).*$')
        self._re_ac_online = re.compile(r'^state:\s*(?P<state>on.line).*$')

    def update(self, queue):
        while True:
            try:
                fg_color = self._fg

                icon = self.insertIcon('bat_full_01.xbm')

                ac_vals = bool(int(open(os.path.join(self._ac, 'online')).read()))
                lastfull = int(open(os.path.join(self._bat, 'energy_full')).read())
                remain = int(open(os.path.join(self._bat, 'energy_now')).read())
                rate = int(open(os.path.join(self._bat, 'voltage_now')).read())

                percent = int(100 / lastfull * remain)
                if percent < 25:
                    fg_color = self._fg_urgent
                    icon = self.insertIcon('bat_empty_01.xbm')
                elif percent < 50:
                    fg_color = self._fg_notice
                    icon = self.insertIcon('bat_low_01.xbm')

                ac = ''
                if ac_vals:
                    mins = (3600.0 * (float(remain) / float(rate))) / 60.0
                    hours = math.floor(mins / 60.0)
                    mins = math.floor(mins - (hours * 60.0))
                    ac = ' %02d:%02d' % (hours, mins)
                    icon = self.insertIcon('ac15.xbm')
                    fg_color = self._fg_notice

                percent = str(percent)+'%'
                output = self.setFgColor((icon), fg_color) + self.pad(percent)
                queue.put({self.__class__.__name__: output})
            except Exception as e:
                self._logger.debug(e)

            time.sleep(self._timeout)

