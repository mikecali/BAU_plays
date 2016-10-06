#!/usr/bin/python
'''This is used to set variables that can be accessed from anywhere within the
project'''

import logging

cmk_server = 'ip-or-hostname'
cmk_server_port = 6557
debug = False
dryrun = False
enable_monitoring = True

enable_rollback = True

#transport = xmlrpcproxy.HTTPProxyTransport({'http': 'http://192.168.56.1:3128',})
#transport = ''


#Setup logging
def init_logging():
    '''By default we log all messages for debugging, only loglevel messages
       of INFO or higher get printed to the screen, log levels are:
       DEBUG INFO WARNING ERROR CRITICAL

       A call to logging a message is simply done as:
       logger.debug('debug message')
       logger.info('info message')
       logger.warn('warn message')
       logger.error('error message')
       logger.critical('critical message')
    '''

    logger_obj = logging.getLogger('ng_sat5_patch')
    logger_obj.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    file_handler = logging.FileHandler('ng_sat5_patch.log')
    file_handler.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    console_handler_format = logging.Formatter('%(levelname)s - %(message)s')
    file_handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_handler_format)
    file_handler.setFormatter(file_handler_format)

    # add the handlers to logger
    logger_obj.addHandler(console_handler)
    logger_obj.addHandler(file_handler)

    return logger_obj

logger = init_logging()
