#!/usr/bin/env python
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

import sys
import os
import re
import types
import time
import subprocess
import logging
import traceback
import inspect
from multiprocessing import Process, Queue
from optparse import OptionParser
from log.centrallogger import CentralLogger, Logger


class utils(object):
    @staticmethod
    def screens(screens = 0):
        """
        try to get number of xinerama screens and return a list of screen numbers.

        first check if parameter value is > 0, if so, use it.

        second check XINERAMA_SCREENS environment variable, which should contain the
        number of screens.

        if the environment variable is not set, try xrandr to get the number of
        connected displays.

        if xrandr fails, return one screen. (-> [0])
        """
        logger = logging.getLogger('utils')

        if screens <= 0:
            logger.debug('try to read environment variable "XINERAMA_SCREENS"')
            screens = os.environ.get('XINERAMA_SCREENS')
        if isinstance(screens, str):
            try:
                screens = int(screens)
            except ValueError:
                logger.error('XINERAMA_SCREENS invalid (%s)' % screens)
                screens = 0
        if not screens:
            try:
                logger.debug('try to use xrandr to determine number of connected screens')
                screens = str(utils.execute('xrandr'))
                screens = len(re.findall(" connected ", screens, re.M))
            except OSError:
                logger.warning('can not execute xrandr')
                screens = 1
        logger.debug('found %d screens' % screens)
        return range(0, screens)

    @staticmethod
    def parse_app(args, regex_list, value = None):
        """
        parse the output on stdout from an application with one or several
        regular expressions.

        return an dictionary with all matches.
        """
        logging.getLogger('utils').debug('parse_app(%s, %s, %s)' % (args, regex_list, value))
        return utils.parse(utils.execute(args, value).split('\n'), regex_list)

    @staticmethod
    def parse(lines, regex_list):
        """
        parse a list of lines with one or several regular expressions.
        matching groups must be named with (?P<name>...).

        all matches are returned as dictionary, where the key is the group
        name with the (maybe multiple) matches as list.
        """
        if not isinstance(regex_list, (types.ListType, types.TupleType)):
            regex_list = [regex_list]

        ret = {}
        for line in lines:
            for regex in regex_list:
                match = regex.match(line)
                if match:
                    for k, v in match.groupdict().iteritems():
                        ret.setdefault(k, []).append(v)

        return ret

    @staticmethod
    def pipe(app, **kwargs):
        """
        execute an application and return an communication object (returned by
        subprocess.Popen(...)).

        all parameters in **kwargs will be used as command line parameters for the
        application. e.g.
            execute('foo', v = True, w = 60, i = '/proc/bar')
               -> foo -v -w 60 -i /proc/bar
        """
        logger = logging.getLogger('utils')

        def _to_param(k, v):
            if isinstance(v, bool):
                return ['-%s' % k]
            return ['-%s' % k, '%s' % str(v)]

        args = [app]
        for k,v in kwargs.items():
            if v is not None:
                args.extend(_to_param(k,v))

        try:
            logger.debug('utils.pipe(%s)' % str(args))
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)
        except OSError as e:
            logger.error('can not execute "%s": %s' % (app, e))
            sys.exit(1)
        return p

    @staticmethod
    def execute(app, value = None, **kwargs):
        """
        execute an application 'app'. if 'value' is unequal None, then it's send
        via stdin to the application.

        all parameters in **kwargs will be used as command line parameters for the
        application. e.g.
            execute('foo', v = True, w = 60, i = '/proc/bar')
               -> foo -v -w 60 -i /proc/bar

        all output on stdout generated by the application is returned.

        if an error occurs, pydzen will be terminated.
        """
        logger = logging.getLogger('utils')

        # if not value: value = ''

        p = utils.pipe(app, **kwargs)
        if value:
            out, err = p.communicate(bytes(value, "UTF-8"))
        else:
            out, err = p.communicate()
        if err:
            logger.error('execute: error: %s' % err)
            sys.exit(1)
        return out

    @staticmethod
    def cache(timeout):
        """
        decorator, to cache the return value of an function for several
        seconds.
        """
        def wrapper(f, cache={}):
            def nfunc():
                key = f
                if key not in cache:
                    cache[key] = [f(), time.time()]
                elif (time.time() - cache[key][1]) >= timeout:
                    cache[key] = [f(), time.time()]
                return cache[key][0]
            return nfunc
        return wrapper

    def onClick(btn, action, string):
        """
        wrapper for dzen's ^ca().
        returns string wrapped by ^ca() and calls script action when
        string is clicked with mouse button btn.

        btn: 1-3, for left, right, middle mouse buttons
        action: path to script to call
        """
        return "^ca(%s, %s) %s ^ca()" % (btn, action, string)


def load_plugins():
    """
    each plugin must define an 'update' method, which returns either a string, an array
    of strings or None.
    """
    from plugin import Plugin, Mode, Position
    logger = Logger(config.LOG_QUEUE)

    sys.path.insert(0, os.path.expanduser(config.PLUGIN_DIR))
    plugins = []
    for p in config.PLUGINS:
        # Plugin is a class
        if '.' not  in p:
            try:
                plugin = __import__(p)
                for name in dir(mod):
                    obj = getattr(mod, name)
                    if inspect.isclass(obj) and isPlugin(obj):
                        # Initialize Plugin class
                        plugInstance = obj()
                        logger.debug('load plugin class: "%s"' % plugInstance)
                        plugInstance.name = plugInstance.__class__.__name__
                        plugins.append(plugInstance)
            except ImportError as e:
                logger.error('error loading plugin class "%s": %s' % (p, e))
        # Plugin is a script
        else:
            try:
                plugin = __import__(p, {}, {}, '*')
                if hasattr(plugin, 'update'):
                    logger.debug('load plugin: "%s"' % p)
                    plugin.name = p
                    plugins.append(plugin)
                else:
                    logger.warning('invalid plugin "%s": no update() function specified' % p)
            except ImportError as e:
                logger.error('error loading plugin "%s": %s' % (p, e))
    sys.path = sys.path[1:]
    return plugins

def isPlugin(plugin):
    if hasattr(plugin, 'update') and plugin.__name__ != 'Plugin':
        return True
    else:
        return False

def init_logging_process():
    logger_proc = CentralLogger(config.LOG_QUEUE)
    logger_proc.daemon = True
    logger_proc.start()

def init_template():
    t = {}
    for i in config.ORDER.keys():
        t[i] = []
        for j in config.ORDER[i]:
            t[i].append(None)
    return t

def read_config_file(file, **defaults):
    """
    try to read the configuration file "file".
    this is a normal python file, which defines several variables. these variables are
    then accessable through the ConfigWrapper object as normal member variables.

    **defaults are default configuration variables, which might be overwritten.
    """
    config = defaults.copy()
    try:
        with open(os.path.expanduser(file)) as f:
            conf = compile(f.read(), str(os.path.expanduser(file)), 'exec')
            exec(conf, {}, config)
    except Exception as e:
        print ('Invalid configuration file: %s' % e)
        sys.exit(1)
    class _ConfigWrapper(dict):
        def __init__(self, *args, **kwargs):
            super(_ConfigWrapper, self).__init__(*args, **kwargs)
        def __getattr__(self, name):
            return self[name]
        def __setattr__(self, name, value):
            self[name] = value
            return self[name]
    return _ConfigWrapper(config)

def configure():
    """
    parse command line parameters, then read config file and return
    an configuration object.
    """
    parser = OptionParser()
    parser.add_option('-c', '--config', dest = 'CONFIG_FILE',
            help = 'specify an alternate pydzenrc file')
    parser.add_option('-p', '--plugins', dest = 'PLUGIN_DIR',
            help = 'specify an alternate plugin directory')
    parser.add_option('-s', '--screens', dest = 'SCREENS', type = 'int',
            help = 'number of Xinerama screen')
    parser.set_defaults(CONFIG_FILE = os.path.join(os.getcwd(), 'pydzenrc'),
            PLUGIN_DIR = os.path.join(os.getcwd(), 'plugins/'),
            SCREENS = 0)

    (options, args) = parser.parse_args()
    config = read_config_file(options.CONFIG_FILE,
            PLUGINS = [],
            LOGLEVEL = logging.WARN,
            SCREENS = options.SCREENS,
            PLUGIN_DIR = options.PLUGIN_DIR)
    return config

def display(template):
    left_text =  config.JOINTS.join(filter(None, template['LEFT']))
    center_text = config.JOINTS.join(filter(None, template['CENTER']))
    right_text = config.JOINTS.join(filter(None, template['RIGHT']))

    write_to_stdin(left_dzen, left_text)
    write_to_stdin(right_dzen, right_text)
    write_to_stdin(center_dzen, center_text)

def write_to_stdin(proc, text):
    proc.stdin.write(bytes(text+'\n', 'utf-8'))
    proc.stdin.flush()

def get_dzen_procs():
    left_proc = subprocess.Popen([os.path.join(config.PYDZEN_PATH, 'scripts/onethirdpanel.sh'), 'l', 'panel-left'], stdin=subprocess.PIPE)
    center_proc = subprocess.Popen([os.path.join(config.PYDZEN_PATH, 'scripts/onethirdpanel.sh'), 'c', 'panel-center'], stdin=subprocess.PIPE)
    right_proc = subprocess.Popen([os.path.join(config.PYDZEN_PATH, 'scripts/onethirdpanel.sh'), 'r', 'panel-right'], stdin=subprocess.PIPE)
    return left_proc, center_proc, right_proc

def get_plugin_procs(plugin_q):
    """
    Starts plugins in a separate process
    """
    plugins = load_plugins()
    procs = []

    # Don't start procs yet, set them up first.
    for p in plugins:
        proc = Process(target=p.update, args=(plugin_q,), name=p.name)
        proc.daemon = True
        procs.append(proc)

    return procs

config = configure()

if __name__ == '__main__':
    init_logging_process()

    logger = Logger(config.LOG_QUEUE)
    logger.info("*** Pydzen Logger initialized  ***")

    # Initalize an empty template to split output
    template = init_template()

    # Start a Dzen instance for each panel alignment
    logger.info("*** Initializing Dzen Processes  ***")
    left_dzen, center_dzen, right_dzen = get_dzen_procs()

    logger.info("*** Initializing Plugin Processes  ***")
    plugin_q = Queue()
    plugin_procs = get_plugin_procs(plugin_q)

    try:
        logger.info("*** Starting Plugin Processes ***")
        for p in plugin_procs:
            p.start()

        while True:
            q = plugin_q.get()

            # Split the queue output for each alignment
            #TODO: Create separate queue for each alignment
            if list(q.keys())[0] in config.ORDER['LEFT']:
                template['LEFT'][config.ORDER['LEFT'].index(list(q.keys())[0])] = str(q[list(q.keys())[0]])
            if list(q.keys())[0] in config.ORDER['CENTER']:
                template['CENTER'][config.ORDER['CENTER'].index(list(q.keys())[0])] = str(q[list(q.keys())[0]])
            if list(q.keys())[0] in config.ORDER['RIGHT']:
                template['RIGHT'][config.ORDER['RIGHT'].index(list(q.keys())[0])] = str(q[list(q.keys())[0]])

            display(template)

    except IOError as e:
        try:
            logger.error(dzen.stderr.read())
            logger.exception(se)
        except Exception as se:
            logger.exception(se)
    except KeyboardInterrupt:
        for p in plugin_procs:
            p.terminate()
        logger.quit()
