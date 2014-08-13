import os
import logging
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
        logging.basicConfig(level = logging.ERROR,
                            filename = os.path.join(os.environ.get('HOME'), '.pydzen/log/Logs.log'))
        self._log = logging.getLogger('pydzen')
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

