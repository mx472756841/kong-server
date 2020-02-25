# -*- coding: utf-8
"""
@author: lanlmeng@qq.com
@file: settings.py
@time: 2020/2/21 18:17
"""


from __future__ import unicode_literals, absolute_import

import logging.config
import os

# 当前目录所在路径
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
# 日志所在目录
LOG_PATH = os.path.join(BASE_PATH, 'logs')
# 临时存储目录
TEMP_PATH = os.path.join(BASE_PATH, 'temp')

# 是否调试模式
DEBUG = False

# *********************** tornado 配置 **********************
HOST = '127.0.0.1'
PORT = 9100
# *********************** tornado 配置 **********************

LOGGING_LEVEL = 'DEBUG' if DEBUG else 'INFO'
LOGGING_HANDLERS = ['console'] if DEBUG else ['file']

# 日志模块配置
if not os.path.exists(LOG_PATH):
    # 创建日志文件夹
    os.makedirs(LOG_PATH)

if not os.path.exists(TEMP_PATH):
    # 创建日志文件夹
    os.makedirs(TEMP_PATH)

logging.config.dictConfig({
    'level': LOGGING_LEVEL,
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(process)d] [%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': LOGGING_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_PATH, 'server.log'),
        }
    },
    'loggers': {
        'common': {
            'handlers': LOGGING_HANDLERS,
            'level': LOGGING_LEVEL,
        }
    }
})
