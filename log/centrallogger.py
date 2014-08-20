import os
import logging
import logging.handlers
import multiprocessing

class CentralLogger(multiprocessing.Process):

    """Logging process. Works with python
    subprocesses and multiprocessing.
    """

    def __init__(self, queue):
        """Reads messages from a queue
        and logs them to a file.

        :queue: the log queue

        """
        multiprocessing.Process.__init__(self)

        self._queue = queue
        self.LOGFILE_NAME = 'log/pydzen.log'
        self._log = logging.getLogger('pydzen')
        self._log.setLevel(logging.ERROR)

        self._handler = logging.handlers.RotatingFileHandler(
                self.LOGFILE_NAME, maxBytes=10*1024*1024, backupCount=3
                )
        self._log.addHandler(self._handler)

        self._log.info('** Central Logger process started **')

    def run(self):
        while True:
            log_level, message = self._queue.get()
            if log_level is None:
                self._log.info('** Shutting down Central Logger **')
                break
            else:
                self._log.log(log_level, message)
        self.terminate()

class Logger():

    """Interface to simplify logging
    with CentralLogger. This class should be
    imported in place of using logging.getLogger().

    example use:

        from log.centrallogger import Logger
        logger = Logger(config.LOG_QUEUE)

        except Exception as e:
            logger.exception(e)
    """

    def __init__(self, queue):
        self._queue = queue

    def info(self, msg):
        self._queue.put((logging.INFO, msg))

    def debug(self, msg):
        self._queue.put((logging.DEBUG, msg))

    def warn(self, msg):
        self._queue.put((logging.WARN, msg))

    def error(self, msg):
        self._queue.put((logging.ERROR, msg))

    def exception(self, msg):
        self._queue.put((logging.CRITICAL, msg))

    def log(self, log_level, msg):
        self._queue.put((log_level, msg))

    def quit(self):
        self._queue.put((None, 'Quit'))

