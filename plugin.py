import os, sys
import traceback
import subprocess

from abc import ABCMeta, abstractmethod
from string import Template
from log.centrallogger import Logger
from pydzen import config, utils
from pluginEnums import Mode, Position

class Plugin(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._mode = Mode.bar
        self._position = Position.none
        self._fg = config.FG_COLOR
        self._bg = config.BG_COLOR

    @abstractmethod
    def update(self):
        pass

    def insertIcon(self, iconName):
        if self._mode == Mode.dzen:
            return "^i(%s)" % (os.path.join(config.ICON_PATH, iconName))
        else:
            return iconName

    def onClick(self, action, string, btn = "1"):
        """
        wrapper for dzen's ^ca().
        returns string wrapped by ^ca() and calls script action when
        string is clicked with mouse button btn.

        btn: 1-3, for left, right, middle mouse buttons,
            defualts to left mouse button
        action: path to script to call
        """

        if self._mode == Mode.dzen:
            result = Template("^ca($btn, $act) $str ^ca()")
        else:
            result = Template("%{A$btn:$act:}$str%{A}")

        return result.substitute(btn, action, string)
