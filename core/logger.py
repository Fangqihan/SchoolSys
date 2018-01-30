# -*- coding: utf-8 -*-   @Time    : 18-1-19 下午7:50
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

import logging
from logging import handlers

from conf.settings import *


def log_generate(**kwargs):
    log_type = kwargs.get('log_type', '')
    id = kwargs.get('id')

    if log_type == 'teacher':
        message = kwargs.get('message', '')
        file_name = LOG_TYPES['teacher']
        logger = logging.getLogger(id)
        logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(LOG_PATH+file_name)
        logger.addHandler(file_handler)

        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        file_handler.setFormatter(file_formatter)

        logger.info(message)
        logger.removeHandler(file_handler)

    elif log_type == 'student':
        message = kwargs.get('message', {})
        file_name = LOG_TYPES['student']
        logger = logging.getLogger(id)
        logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(LOG_PATH + file_name)
        logger.addHandler(file_handler)

        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        file_handler.setFormatter(file_formatter)

        logger.info(message)
        logger.removeHandler(file_handler)

    elif log_type == 'admin':
        message = kwargs.get('message', {})
        file_name = LOG_TYPES['admin']
        logger = logging.getLogger('admin')
        logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(LOG_PATH + file_name)
        logger.addHandler(file_handler)

        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        file_handler.setFormatter(file_formatter)

        logger.info(message)
        logger.removeHandler(file_handler)



