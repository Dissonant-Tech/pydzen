import os, sys

from string import Template
from abc import ABCMeta, abstractmethod
from pluginEnums import Mode, Position
from multiprocessing import Queue

from pydzen import config, utils

class Plugin(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._mode = Mode.bar
        self._position = Position.none
        self._log_queue = config.LOG_QUEUE
        self._fg = config.FG_COLOR
        self._bg = config.BG_COLOR

    @abstractmethod
    def update(self, queue):
        pass

    def setFgColor(self, text, color):
        if self._mode == Mode.dzen:
            result = Template("^fg($cl) $txt ^fg()")
        if self._mode == Mode.bar:
            result = Template("%{F$cl} $txt %{F-}")
        return result.substitute(cl = color, txt = text);

    def setBgColor(self, text, color):
        if self._mode == Mode.dzen:
            result = Template("^bg($cl) $txt ^bg()")
        if self._mode == Mode.bar:
            result = Template("%{B$cl} $txt %{B-}")
        return result.substitute(cl = color, txt = text);

    def insertIcon(self, iconName):
        if self._mode == Mode.dzen:
            return "^i(%s)" % (os.path.join(config.ICON_PATH, iconName))
        else:
            return iconName

    def onClick(self, action, string, button = "1"):
        """
        wrapper for dzen's ^ca().
        returns string wrapped by ^ca() and calls script action when
        string is clicked with mouse button btn.

        button: 1-3, for left, right, middle mouse buttons,
            defualts to left mouse button
        action: path to script to call
        """

        if self._mode == Mode.dzen:
            result = Template("^ca($btn, $act) $stn ^ca()")
        else:
            result = Template("%{A$btn:$act:} $stn %{A}")

        return result.substitute(btn = button, act = action, stn = string)
