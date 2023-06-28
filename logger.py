import logging

"""
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
"""
class DHLLogger(logging.Logger):
    """
    dict_keys(['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename', 'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'reqid', 'server', 'app', 'component', 'subcomponent'])

    """

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if not extra:
            extra = {}
        for k in ['reqid', 'server', 'app', 'component', 'subcomponent']:
            v = 'NA' if not k else extra.get(k)
            extra[k] = f'{k}: {v}'
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)


logger = DHLLogger(__name__)

handler = logging.StreamHandler()
handler2 = logging.FileHandler(filename="app.log")

FORMAT = '[%(asctime)s.%(msecs)03d] %(levelname)s  %(filename)s %(funcName)s %(lineno)s [%(reqid)s] [%(server)s] [%(app)s] [%(component)s] [%(subcomponent)s]- %(message)s'
formatter = logging.Formatter(FORMAT)

handler.setFormatter(formatter)
handler2.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(handler2)
