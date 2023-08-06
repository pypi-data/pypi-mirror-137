import datetime
import logging
from dl2050utils.core import oget

LOG_FORMAT = '\
%(name)s  %(levelname)s - %(asctime)s - %(product)s:%(client)s:%(instance)s:%(service)s - \
%(label)s - %(label2)s - %(duration).3f - %(message)s'

def parse_msg(d, level=0):
    if d is None: return 'null'
    if type(d) in [int, float]: return str(d)
    if isinstance(d, str): return d.replace('\n', ' ')
    if isinstance(d, datetime.datetime): return d.strftime("%Y-%m-%Y %H:%M:%S")
    if type(d) is list: return f'[#{len(d)}]'
    if type(d) is not dict: return f'OBJECT-{type(d)}'
    s = '{'
    for key, val in d.items():
        if isinstance(d[key], dict):
            s += f'{key}:'+'{...}'
        elif type(d[key]) is list:
            s += f'{key}:[#{len(d)}]'
        else:
            s += f'{key}:{val}'
        s += ', '
    return s[:-2]+'}'

class AppLog():
    def __init__(self, cfg, service='rest'):
        global loggers
        self.msg_prefix = {
            'product': oget(cfg, ['app','product'], '_PRODUCT_'),
            'client': oget(cfg, ['app','client'], '_CLIENT_'),
            'instance': oget(cfg, ['app','instance'], '_INSTANCE_'),
            'service': service,
        }
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('APPLOG')
        logger.propagate = False
        while len(logger.handlers):
            logger.removeHandler(logger.handlers[0])
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        formatter = logging.Formatter(LOG_FORMAT)
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        self.LOG_LEVELS = {
            1: logger.debug,
            2: logger.info,
            3: logger.warning,
            4: logger.error,
            5: logger.critical
        }
        
    def __call__(self, level=3, ts0=None, label=None, label2=None, msg=''):
        if not isinstance(level, int) or level<1 or level>5: return
        log_f = self.LOG_LEVELS[level]
        log_msg = self.msg_prefix
        log_msg['label'],log_msg['label2'],log_msg['duration'] = label,label2,ts0 or 0
        s = parse_msg(msg)
        log_f(s, extra=log_msg)

    def log(self, *args, **kwargs): self.__call__(*args, **kwargs)
