import os
import sys
from log.centrallogger import Logger
import subprocess

from pydzen import config

logger = Logger(config.LOG_QUEUE)

def update(queue):
    try:
        # Open a pipe to xtitle output
        sub = subprocess.Popen(['xtitle', '-s'], stdout=subprocess.PIPE)

        while True:
            line = sub.stdout.readline()
            
            # FIXME for some reason decoding the bytes makes line = None
            # but straight conversion to string leaves b'title...\n'
            line = str(line)
            line = line[2:-3]

            title = (line[:45]+'...') if len(line) > 45 else line
            queue.put({'plugins.title': title})
    except Exception as e:
        logger.exception(e)
