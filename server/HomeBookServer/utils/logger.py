# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

import logging
import logging.config
from configs import Config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logger.conf')
logging.config.fileConfig(log_file_path)

def getLogger(lname=None):
    _logger=None
    if lname:
        _logger=logging.getLogger(lname)
    elif Config.LOGGER:
        _logger= logging.getLogger(Config.LOGGER)
    else:
        _logger= logging.getLogger("root")
    return _logger

logger=getLogger()