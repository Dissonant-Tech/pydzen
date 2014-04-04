import os
import sys
import logging
import subprocess

logger = logging.getLogger('plugins.title')

def update(queue):
    try:
        # Open a pipe to xtitle output
        sub = subprocess.Popen(['xtitle', '-s'], stdout=subprocess.PIPE)

        while True:
            line = sub.stdout.readline()
            line = str(line)
            title = (line[:45]+'...') if len(line) > 45 else line
            queue.put({'plugins.title': title})
    except Exception as e:
        logger.exception(e)
