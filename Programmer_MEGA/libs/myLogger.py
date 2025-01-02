import sys 
import logging 
import io
from logging.handlers import RotatingFileHandler

FILE_FORMAT    = "[%(levelname)s] | [%(asctime)s] (%(filename)s:%(lineno)d) | %(message)s"
CONSOLE_FORMAT = "%(message)s"

FILESIZE = 10e6
MAX_FILES = 10

class NoParsingFilter(logging.Filter):
    def filter(self, record):
        forbiddenWords = [
            'PING ',
            'PONG',
            'sending keepalive ping',
            'received keepalive pong',
            'connection open',
            'connection closed'
        ]
        message = record.getMessage()
        for x in forbiddenWords:
            if x in message:
                return False
        return True
        
class StdoutLogger(io.TextIOBase):
    def __init__(self, level):
        self.level = level
        self.buffer = ''

    def write(self, buf):
        self.buffer += buf
        if '\n' in self.buffer:
            for line in self.buffer.splitlines():
                self.level(line.rstrip().encode(encoding='utf-8',errors='ignore'))
            self.buffer = ''

class StderrLogger(io.TextIOBase):
    def __init__(self, level):
        self.level = level
        self.buffer = ''

    def write(self, buf):
        self.buffer += buf
        if '\n' in self.buffer:
            for line in self.buffer.splitlines():
                self.level(line.rstrip().encode(encoding='utf-8',errors='ignore'))
            self.buffer = ''

def setup_stdout_stderr_logging():
    stdout_logger = logging.getLogger('STDOUT')
    sys.stdout = StdoutLogger(stdout_logger.info)
    stderr_logger = logging.getLogger('STDERR')
    sys.stderr = StderrLogger(stderr_logger.warning)

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = '\033[32m'
    blue = '\033[90m'
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = CONSOLE_FORMAT
    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: green + format + reset
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt , "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setLogger( filename , loggingType , customFormatter = True):
    #loggingType = logging.DEBUG
    logger = logging.getLogger()
    logger.setLevel(loggingType)
    formatter = logging.Formatter(FILE_FORMAT)
    file_handler_new = RotatingFileHandler(f"{filename}", maxBytes=FILESIZE, backupCount=MAX_FILES)
    file_handler_new.setLevel(loggingType)
    file_handler_new.setFormatter(formatter)
    file_handler_new.addFilter(NoParsingFilter())
    file_handler_new.encoding = 'utf-8'
    logger.addHandler(file_handler_new)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(loggingType)
    if customFormatter:
        console_handler.setFormatter(CustomFormatter())
        console_handler.addFilter(NoParsingFilter())
    logger.addHandler(console_handler)

    setup_stdout_stderr_logging()
