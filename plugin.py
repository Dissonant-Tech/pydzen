import os, sys
from string import Template
from abc import ABCMeta, abstractmethod
from multiprocessing import Queue
from enum import Enum

from pydzen import config, utils
from log.centrallogger import Logger

class Mode(Enum):
    dzen = 1
    bar = 2

class Position(Enum):
    left = 1
    center = 2
    right = 3
    none = 4

class Plugin(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._mode = Mode.dzen
        self._position = Position.none
        self._priority = 50
        self._log_queue = config.LOG_QUEUE
        self._logger = Logger(self._log_queue)
        self._fg = config.FG_COLOR
        self._bg = config.BG_COLOR
        self._fg_urgent = config.FG_COLOR_URGENT
        self._fg_notice = config.FG_COLOR_NOTICE

    @abstractmethod
    def update(self, queue):
        pass

    def setFgColor(self, text, color):
        if self._mode == Mode.dzen:
            result = Template("^fg($cl)$txt^fg()")
        if self._mode == Mode.bar:
            result = Template("%{F$cl}$txt%{F-}")
        return result.substitute(cl = color, txt = text);

    def setBgColor(self, text, color):
        if self._mode == Mode.dzen:
            result = Template("^bg($cl)$txt^bg()")
        if self._mode == Mode.bar:
            result = Template("%{B$cl}$txt%{B-}")
        return result.substitute(cl = color, txt = text);

    def insertIcon(self, icon, useAbsPath = False):
        result = ""
        template = "^i(%s)"

        if self._mode == Mode.dzen:
            if useAbsPath:
                result = template % icon
            result = template % (os.path.join(config.ICON_PATH, icon))
        else:
            result = iconName

        return result

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
            result = Template("^ca($btn, $act)$stn^ca()")
        else:
            result = Template("%{A$btn:$act:}$stn%{A}")

        return result.substitute(btn = button, act = action, stn = string)
    
    def pad(self, text):
        """
        Adds a space before and after input.

        text: string input
        """
        return " " + text + " " 
