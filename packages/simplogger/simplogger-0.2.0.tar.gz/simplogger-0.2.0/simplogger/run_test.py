import unittest
from logger import simplog
import logging
import logging.handlers
import os
import sys

class AAASimpLogInit(unittest.TestCase):

    # Verifies can crete the object
    def test_AAA_init_simplog(self):
        try:
            _ = simplog('Init')
        except:
            raise Exception('Unable to initialize the simplog')

    # Attempts to create a simplog given it already exists
    def test_AAB_init_preexisting_simplog(self):
        self.assertEqual(simplog('Init'), simplog('Init'),\
            msg='SimpLog were not the same despite being fed the same logkey')

    # Attempts to create a simplog with parameters given it already exists
    def test_AAC_init_preexisting_simplog_with_new_params(self):
        # Disable the logger so it does not output anything
        logging.disable(logging.CRITICAL)
        log = simplog('Init', file='test.logs')
        self.assertLogs(log.getLogger(), log.WARNING)
        logging.disable(logging.NOTSET)

class AABSimpLogBasicUse(unittest.TestCase):

    def test_AAA_getLogger(self):
        log = simplog('BasicUse')
        self.assertEqual(type(log.getLogger()),logging.Logger,\
            msg='Did not return proper logger with getLogger')
        self.assertEqual(log.getLogKey(),'BasicUse',\
            msg='Did not return proper logkey with getLogKey')

    def test_AAB_viewHandlers(self):
        log = simplog('BasicUse.viewHandlers')
        # Verify new log has no handlers
        self.assertEqual(log.hasHandlers(),False,\
            msg='hasHandlers() returned True when should be false')
        self.assertEqual(len(log.getHandlers()), 0)
        # Add a handler
        log.addHandler(htype='stream')
        # Verify that hashandlers is now true and has one in list
        self.assertEqual(log.hasHandlers(),True,\
            msg='hasHandlers() returned True when should be false')
        self.assertEqual(len(log.getHandlers()), 1)

        log.getHandlers()[-1].close()

    def test_AAB_logStuff(self):
        log = simplog('BasicUse.logstuff')
        logger = log.getLogger()
        logging.disable(logging.CRITICAL)
        # DEBUG
        if sys.version_info[1] >= 10 and sys.version_info[0] == 3:
            self.assertNoLogs(logger, logging.DEBUG)
        log.debug('DEBUG-message')
        self.assertLogs(logger, logging.DEBUG)
        # INFO
        if sys.version_info[1] >= 10 and sys.version_info[0] == 3:
            self.assertNoLogs(logger, logging.INFO)
        log.info('INFO-message')
        self.assertLogs(logger, logging.INFO)
        # WARN/ WARNING
        if sys.version_info[1] >= 10 and sys.version_info[0] == 3:
            self.assertNoLogs(logger, logging.WARNING)
        log.warning('WARNING-message')
        self.assertLogs(logger, logging.INFO)
        # ERROR
        if sys.version_info[1] >= 10 and sys.version_info[0] == 3:
            self.assertNoLogs(logger, logging.ERROR)
        log.error('ERROR-message')
        self.assertLogs(logger, logging.ERROR)

        # CRITICAL
        if sys.version_info[1] >= 10 and sys.version_info[0] == 3:
            self.assertNoLogs(logger, logging.CRITICAL)
        log.critical('CRITICAL-message')
        self.assertLogs(logger, logging.CRITICAL)

        logging.disable(logging.NOTSET)

    def test_AAC_raiseException(self):
        log = simplog('BasicUse.logstuff')
        logging.disable()
        self.assertRaises(Exception, log.exception, \
                                    'exception w/ error', err=True)
        self.assertRaises(ValueError, log.exception, \
                                    'exception w/ ValueError', err=ValueError)

        logging.disable(logging.NOTSET)


class AACSimpLogHandlers(unittest.TestCase):

    # Creates the AAA
    def test_AAA_createHandlers_stream(self):
        log = simplog('Handlers')
        hndlr = log.createHandler(htype='stream')
        self.assertEqual(logging.StreamHandler,\
            type(hndlr), msg='Failed to create stream (console) handler')

    def test_AAA_createHandlers_file(self):
        log = simplog('Handlers')
        hndlr = log.createHandler(htype='file', filename='simplog_unittest.logs')
        self.assertEqual(logging.FileHandler,\
            type(hndlr),msg='Failed to create file handler')
        hndlr.close()
        os.remove('simplog_unittest.logs')

    def test_AAA_createHandlers_WatchedFile(self):
        log = simplog('Handlers')
        hndlr = log.createHandler(htype='watch', filename='simplog_unittest.logs')
        self.assertEqual(logging.handlers.WatchedFileHandler,\
            type(hndlr), msg='Failed to create watched file handler')
        hndlr.close()
        os.remove('simplog_unittest.logs')

    def test_AAA_createHandlers_RotatingFile(self):
        log = simplog('Handlers')
        hndlr = log.createHandler(htype='rotating', filename='simplog_unittest.logs')
        self.assertEqual(logging.handlers.RotatingFileHandler,\
            type(hndlr), msg='Failed to create watched file handler')
        hndlr.close()
        os.remove('simplog_unittest.logs')

    def test_AAA_createHandlers_TimedRotatingFile(self):
        log = simplog('Handlers')
        hndlr = log.createHandler(htype='timed', filename='simplog_unittest.logs')
        self.assertEqual(logging.handlers.TimedRotatingFileHandler,\
            type(hndlr), msg='Failed to create timed rotating file handler')
        hndlr.close()
        os.remove('simplog_unittest.logs')

    def test_AAA_createHandlers_Null(self):
        log = simplog('Handlers')
        hndlr = log.createHandler(htype='null')
        self.assertEqual(logging.NullHandler,type(hndlr),
            msg='Failed to create timed null handler')
        hndlr.close()

    def test_AAB_addHandler(self):
        log = simplog('Handlers')
        log.addHandler(htype='stream')
        log.getHandlers()[-1].close()

    def test_AAB_addHandlerFromLogging(self):
        log = simplog('Handlers')
        log.addHandler(logging.StreamHandler())
        log.getHandlers()[-1].close()

if __name__ == '__main__':
    unittest.main()
