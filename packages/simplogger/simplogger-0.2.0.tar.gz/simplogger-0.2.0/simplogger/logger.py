from datetime import datetime
from pathlib import Path
import logging
import logging.handlers
import sys

class simplog():

    cls_logger = None

    dflt_format = logging.Formatter(\
                '%(asctime)s | %(name)s | %(levelname)s - %(message)s')
    simplogs = {}

    CRITICAL, WARNING, WARN, INFO, DEBUG = \
        logging.CRITICAL, logging.WARNING, logging.WARN, \
        logging.INFO, logging.DEBUG

    # Overriden the current so that way if simplog already exists, we get that
    #   This is to make it more similar to current logger behavior
    @staticmethod
    def __new__(cls, *args, **kargs):
        logkey = args[0]
        # If already exists, return it
        if logkey in cls.simplogs:
            if len(args) > 1 or len(kargs) > 0:
                SLog = cls.simplogs[logkey]
                SLog.warning('Tried calling for a pre-existing simplog '+\
                                     'with arguments or key arguments. '+\
                                     'Returning original logger and its params')

                return SLog
            return cls.simplogs[logkey]
        else:
            cls.simplogs[logkey] = super(simplog, cls).__new__(cls)
            return cls.simplogs[logkey]

    def __init__(self, *args, **kargs):

        # Define variables
        self.logkey = args[0]

        # Get the actual logger
        self.logger = logging.getLogger(self.logkey)

        if any(('output_file' in kargs, 'file_lvl' in kargs)):
            params = {}
            for pkey, kkey in (('output_file','output_file'),\
                               ('mode','file_mode'),('delay','file_delay'),\
                               ('encoding','file_encoding')):
                if kkey in kargs:
                    params[pkey] = kargs.get(kkey)
            self.addHandler(htype='file', **params)

        if kargs.get('console_output',False):
            if 'console_lvl' in kargs:
                self.addHandler(htype='stream', h_lvl=kargs.get('console_lvl'))
            else:
                self.addHandler(htype='stream')




    ''' Allows access to the logger '''
    # Returns logger
    def getLogger(self):
        return self.logger
    # Returns key
    def getLogKey(self):
        return self.logkey
    # Returns boolean if has handlers
    def hasHandlers(self):
        return self.getLogger().hasHandlers()
    # Returns list of handlers
    def getHandlers(self):
        return self.getLogger().handlers
    # Returns boolean if has filters
    def hasFilters(self):
        return len(self.getFilters()) > 0
    # Returns list of filters
    def getFilters(self):
        return self.getLogger().filters

    # Modifies the loggers level
    def setLevel(self, new_lvl):
        self.getLogger().setLevel(self.__to_correct_lvl(new_lvl))
    # Disables a level
    def disable(self, *args, **kargs):
        if len(args) == 1 and isinstance(args[0], int):
            lvl = args[0]
        else:
            lvl = kargs.get('level', logging.CRITICAL)
        if sys.version_info[0] == 3 and sys.version_info[1] > 7:
            self.getLogger().disable(level=level)
        else:
            self.getLogger().disable(level)
    # Returns if enabled for that level
    def isEnabledFor(self, lvl):
        return self.getLogger().isEnabledFor(lvl)
    # Gets effective level
    def getEffectiveLevel(self):
        return self.getLogger().getEffectiveLevel()
    # Returns child of that object
    def getChild(self, suffix, return_logger=False):
        if return_logger:
            return self.getLogger().getChild(suffix)
        else:
            curLogKey = self.getLogKey()
            if curLogKey[-1] == '.' or suffix[0] == '.':
                return simplog(curLogKey+suffix)
            else:
                return simplog(curLogKey + '.' + suffix)
    def findCaller(stack_info=False, stacklevel=1):
        return self.getLogger().findCaller(stacl_info=stack_info, \
                                            stacklevel=stacklevel)
    def handle(self, record):
        self.getLogger().handle(record)

    def removeHandler(self, val):
        if isinstance(val, int):
            handlers = self.getHandlers()
            if val < 0 or val >= len(handlers):
                raise IndexError(f'Tried removing handler #{val}, but only '+\
                                 f'has {len(handlers)}')
            self.getLogger().removeHandler(handlers[val])
        elif isinstance(val, logging.handler):
            self.getLogger().removeHandler(val)

    def createHandler(self, **kargs):

        htype = kargs.get('htype', None)
        if htype is None:
            raise ValueError('Must provide karg \'htype\' for Handler type')
        if isinstance(htype, str):
            htype = self.__str_to_handler(htype)

        if htype == logging.StreamHandler:
            if 'stream' in kargs:
                return logging.StreamHandler(stream=kargs.get('stream'))
            return logging.StreamHandler()
            # \/ have similar preprocessing steps, so we can merge them
        elif any((htype==logging.FileHandler,\
                    htype==logging.handlers.WatchedFileHandler,\
                    htype==logging.handlers.RotatingFileHandler, \
                    htype==logging.handlers.TimedRotatingFileHandler)):

            params = {'delay':kargs.get('delay', False),\
                      'encoding':kargs.get('encoding',None)}

            # Handle file name (if path and before 3.6, turn to str)
            filename = kargs.get('filename',self.getFileNameFromTime())
            if sys.version_info[1] < 6 and isinstance(filename, Path):
                filename = str(filename)
            if 'log_dir' in kargs:
                filename = os.path.join(kargs.get('log_dir'),filename).__str__()

            # Actual creation of the different handlers
            if htype == logging.FileHandler:
                if sys.version_info[1] >= 9:
                    return logging.FileHandler(filename,\
                                        mode=kargs.get('mode','a'),\
                                        delay=kargs.get('delay',False),\
                                        encoding=kargs.get('encoding',None),\
                                        errors=kargs.get('errors',None))
                else:
                    return logging.FileHandler(filename,\
                                        mode=kargs.get('mode','a'),\
                                        delay=kargs.get('delay',False),\
                                        encoding=kargs.get('encoding',None))
            elif htype == logging.handlers.RotatingFileHandler:
                if sys.version_info[1] >= 9:
                    return logging.handlers.RotatingFileHandler(filename, \
                                            mode=kargs.get('mode','a'),\
                                            backupCount=kargs.get('backupCount'),\
                                            maxBytes=kargs.get('maxBytes',0),\
                                            delay=kargs.get('delay',False),\
                                            encoding=kargs.get('encoding',None),\
                                            errors=kargs.get('errors',None))
                else:
                    return logging.handlers.RotatingFileHandler(filename, \
                                            mode=kargs.get('mode','a'),\
                                            backupCount=kargs.get('backupCount'),\
                                            maxBytes=kargs.get('maxBytes',0),\
                                            delay=kargs.get('delay',False),\
                                            encoding=kargs.get('encoding',None))
            elif htype == logging.handlers.TimedRotatingFileHandler:
                if sys.version_info[1] >= 9:
                    return logging.handlers.TimedRotatingFileHandler(filename, \
                                        when=kargs.get('when','h'),\
                                        backupCount=kargs.get('backupCount',0),\
                                        utc=kargs.get('utc',False),\
                                        atTime=kargs.get('atTime',None),\
                                        delay=kargs.get('delay',False),\
                                        encoding=kargs.get('encoding',None),\
                                        errors=kargs.get('errors',None))
                else:
                    return logging.handlers.TimedRotatingFileHandler(filename, \
                                        when=kargs.get('when','h'),\
                                        backupCount=kargs.get('backupCount',0),\
                                        utc=kargs.get('utc',False),\
                                        atTime=kargs.get('atTime',None),\
                                        delay=kargs.get('delay',False),\
                                        encoding=kargs.get('encoding',None))

            elif htype == logging.handlers.WatchedFileHandler:
                if sys.version_info[1] >= 9:
                    return logging.handlers.WatchedFileHandler(filename,\
                                        mode=kargs.get('mode','a'),\
                                        delay=kargs.get('delay',False),\
                                        encoding=kargs.get('encoding',None),\
                                        errors=kargs.get('errors',None))
                else:
                    return logging.handlers.WatchedFileHandler(filename,\
                                        mode=kargs.get('mode','a'),\
                                        delay=kargs.get('delay',False),\
                                        encoding=kargs.get('encoding',None))

        elif sys.version_info[1] >= 1 and htype == logging.NullHandler:
            return logging.NullHandler()
        else:
            raise NotImplementedError('Other htypes are not currently '+\
                        'supported, but can be manually added by using '+\
                        'using simplog.addHandler(hndlr), where hndlr is\n'+\
                        'a handler made using the logging module')

    def addHandler(self, *args, **kargs):
        # If provided a pos arg, it should be a handler object, if so add it
        if len(args) == 1 and isinstance(args[0], logging.Handler):
            self.getLogger().addHandler(args[0])
            return
        elif len(args) != 0: # If not 1 or 0, raise error
            raise TypeError('Expected a handler or a list of kargs to make '+\
                                                                    'a handler')

        # Create a handler with given kargs, and then add that handler
        self.getLogger().addHandler(self.createHandler(**kargs))

        if self.dflt_format is not None:
            self.getHandlers()[-1].setFormatter(self.dflt_format)
        if 'h_lvl' in kargs:
            self.getHandlers()[-1].setLevel(kargs.get('h_lvl'))
        if 'formatter' in kargs or 'format' in kargs:
            format = kargs.get('formatter', kargs.get('format'))
            self.getHandlers()[-1].setFormatter(self.__format(format))

    def addFilter(self, *args, **kargs):
        self.logger.addFilter(*args, **kargs)

    def filter(self, *args, **kargs):
        return self.logger.filter(*args, **kargs)

    ''' Log fxns '''
    def log(self, *args, **kargs):
        self.getLogger().log(*args, **kargs)
    def debug(self, *args, **kargs):
        self.getLogger().debug(*args, **kargs)
    def info(self, *args, **kargs):
        self.getLogger().info(*args, **kargs)
    def warn(self, *args, **kargs):
        self.warning(*args, **kargs)
    def warning(self, *args, **kargs):
        self.getLogger().warning(*args, **kargs)
    def error(self, *args, **kargs):
        self.getLogger().error(*args, **kargs)
    def critical(self, *args, **kargs):
        self.getLogger().critical(*args, **kargs)
    def exception(self, *args, **kargs):
        if 'err' in kargs:
            err = kargs.pop('err')
            raise_err = True
        else:
            raise_err = False
        self.getLogger().exception(*args, **kargs)
        if raise_err:
            if err is True:
                raise Exception(args[0])
            else:
                raise err(args[0])

    ''' Static Utility Methods '''
    @staticmethod
    def getFileNameFromTime():
        return datetime.now().strftime('%m-%d-%Y-%H-%M-%S').replace('.','_')+'.logs'

    @staticmethod
    def __str_to_handler(val):
        if not isinstance(val, str):
            raise TypeError('Expected string')
        val = val.lower()
        if val in ('stream', 'streamhandler'):
            return logging.StreamHandler
        elif val in ('file', 'filehandler'):
            return logging.FileHandler
        elif val in ('null', 'nullhandler', 'none', 'nonehandler'):
            return logging.NullHandler
        elif val in ('watchfile', 'watch', 'watchfilehandler', 'watchhandler'):
            return logging.handlers.WatchedFileHandler
        elif val in ('rotatingfilehandler','rotatingfile', 'rotating'):
            return logging.handlers.RotatingFileHandler
        elif val in ('timedrotatingfilehandler', 'timedrotatingfile', \
                            'timedrotating','timed','time'):
            return logging.handlers.TimedRotatingFileHandler
        elif val in ('sockethandler', 'socket'):
            return logging.handlers.SocketHandler
        elif val in ('datagramhandler', 'datagram'):
            return logging.handlers.DatagramHandler
        elif val in ('sysloghandler', 'syslog', 'sys'):
            return logging.handlers.SysLogHandler
        elif val in ('nteventloghandler', 'nteventLog', 'ntevent'):
            return logging.handlers.NTEventLogHandler
        elif val in ('smtphandler', 'smtp'):
            return logging.handlers.SMTPHandler
        elif val in ('memoryhandler', 'memory', 'mem'):
            return logging.handlers.MemoryHandler
        elif val in ('httphandler', 'http'):
            return logging.handlers.HTTPHandler
        elif val in ('queuehandler', 'queue'):
            return logging.handlers.QueueHandler
        elif val in ('queuelistener', 'listener'):
            return logging.handlers.QueueListener

    @staticmethod
    def __to_correct_lvl(lvl):
        # Allows conversion from string
        if isinstance(lvl, str):
            lvl = lvl.lower()
            if lvl in ('notset', 'not set', 'none'):
                return 0
            elif lvl in ('debug'):
                return 10
            elif lvl in ('info', 'information'):
                return 20
            elif lvl in ('warn', 'warning'):
                return 30
            elif lvl in ('error'):
                return 40
            elif lvl in ('critical', 'fatal'):
                return 50
            else:
                raise ValueError('Expected debug, info, warn, '+\
                                    'error, or critical')
        elif isinstance(lvl, int):
            return lvl

    ''' Class parameters and class utility functions '''
    @classmethod
    def __setup_simplog_logger(cls):
        logger = logging.getLogger('simplog')
        logger.setLevel(logging.WARNING)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        if cls.dflt_format is not None:
            console_handler.setFormatter(cls.dflt_format)
        cls.cls_logger = logger

    @classmethod
    def __get_preset_dflt_formats(cls, val):
        if val == 0:
            return None
        elif val == 1:
            return logging.Formatter\
                ('%(levelname)s - %(message)s', "%")
        elif val == 2:
            return logging.Formatter\
                ('%(name)s | %(levelname)s - %(message)s', "%")
        elif val == 3:
            return logging.Formatter\
                ('%(asctime)s | %(name)s | %(levelname)s - %(message)s',\
                    '%H:%M')
        elif val == 4:
            return logging.Formatter\
                ('%(asctime)s | %(name)s | %(levelname)s - %(message)s',\
                    '%H:%M:%S')
        elif val == 5:
            return logging.Formatter\
                ('%(asctime)s | %(name)s | %(levelname)s - %(message)s',\
                    '%m-%d %H:%M')
        elif val == 6:
            return logging.Formatter\
                ('%(asctime)s | %(name)s | %(levelname)s - %(message)s',\
                    '%m-%d %H:%M:%S')
        elif val == 7:
            return logging.Formatter\
                ('%(asctime)s | %(name)s | %(levelname)s - %(message)s',\
                    '%Y-%m-%d %H:%M:%S')
        elif val == 8:
            return logging.Formatter\
                ('%(asctime)s | %(name)s | %(levelname)s - %(message)s',\
                    '%m-%d-%Y %H:%M:%S')

    @classmethod
    def __format(cls, formatting):
        if isinstance(formatting, str):
            return logging.Formatter(formatting)
        elif isinstance(formatting, logging.Formatter):
            return formatting
        elif isinstance(formatting, int):
            return cls.__get_preset_dflt_formats(formatting)
        else:
            raise TypeError('Expected str, formatter obj, or int for a preset')

    @classmethod
    def set_dflt_format(cls, formatting):
        cls.dflt_format = cls.__format(formatting)

    @classmethod
    def remove_dflt_format(cls):
        cls.dflt_format = None

    ''' Other Utility fxns '''
    def __gt__(self, other):
        if isinstance(other, simplog):
            return other.getLogger().__gt__(other.getLogger())
        elif isinstance(other, logging.logger):
            return other.getLogger().__gt__(other)
        else:
            try:
                return other.getLogger().__gt__(other)
            except:
                self.exception('Attempted to perform > between this simplog '+\
                        'and another object of type {type(other)} and failed.')
    def __ge__(self, other):
        if isinstance(other, simplog):
            return other.getLogger().__ge__(other.getLogger())
        elif isinstance(other, logging.logger):
            return other.getLogger().__ge__(other)
        else:
            try:
                return other.getLogger().__ge__(other)
            except:
                self.exception('Attempted to perform >= between this simplog '+\
                        'and another object of type {type(other)} and failed.')
    def __lt__(self, other):
        if isinstance(other, simplog):
            return other.getLogger().__lt__(other.getLogger())
        elif isinstance(other, logging.logger):
            return other.getLogger().__lt__(other)
        else:
            try:
                return other.getLogger().__lt__(other)
            except:
                self.exception('Attempted to perform < between this simplog '+\
                        'and another object of type {type(other)} and failed.')
    def __le__(self, other):
        if isinstance(other, simplog):
            return other.getLogger().__le__(other.getLogger())
        elif isinstance(other, logging.logger):
            return other.getLogger().__le__(other)
        else:
            try:
                return other.getLogger().__le__(other)
            except:
                self.exception('Attempted to perform <= between this simplog '+\
                        'and another object of type {type(other)} and failed.')

    def __eq__(self, other):
        if isinstance(other, simplog):
            return other.getLogger().__eq__(other.getLogger())
        elif isinstance(other, logging.logger):
            return other.getLogger().__eq__(other)
        else:
            try:
                return other.getLogger().__eq__(other)
            except:
                self.exception('Attempted to perform == between this simplog '+\
                        'and another object of type {type(other)} and failed.')

    def __hash__(self):
        return (self.getLogger(), self.logkey).__hash__()

    def __str__(self):
        return f'SimpLog({self.getLogger().__str__()})'


    ''' Other class variables '''

    __doc__ = '\tSimplog is a wrapper object for loggers in order to reduce \n'+\
              '\tthe complexity of the logging library.  Although logging is\n'+\
              '\ta simple library, this reduces the amount of effort needed \n'+\
              '\tto use it for other applications.  For the logger\'s \n'+\
              '\t__doc__, use simplog.getLogger().__doc__'

    '''
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
    '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
    '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
    '__str__', '__subclasshook__', '__weakref__', '_cache', '_log', 'addFilter',
    'addHandler', 'callHandlers', 'critical', 'debug', 'disabled', 'error',
    'exception', 'fatal', 'filter', 'filters', 'findCaller', 'getChild',
    'getEffectiveLevel', 'handle', 'handlers', 'hasHandlers', 'info',
    'isEnabledFor', 'level', 'log', 'makeRecord', 'manager', 'name', 'parent',
    'propagate', 'removeFilter', 'removeHandler', 'root', 'setLevel', 'warn',
    'warning']
    '''
