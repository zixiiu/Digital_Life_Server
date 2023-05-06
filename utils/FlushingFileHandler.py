import logging
import os
import time


class FlushingFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=False, formatter=None):
        super().__init__(filename, mode, encoding, delay)
        self.formatter = formatter
    def emit(self, record):
        super().emit(record)
        try:
            self.nice_try(record)
        except IOError:
            time.sleep(0.2)
            self.nice_try(record)

    def nice_try(self, record):
        with open('log_async.log', 'a') as f:
            f.write(self.formatter.format(record) + '\n')
