# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

import logging

from configs import Config

logging.basicConfig(level=Config.LOG_LEVEL,
    format='%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s: %(message)s')
    
logger=logging.getLogger()