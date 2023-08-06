#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import sys
import os
import traceback
import colorlog
import logging
from logging.handlers import TimedRotatingFileHandler

_LOG_DIR = './logs'
_APP_LOGS = {
    'run.log': logging.INFO, 
    'err.log': logging.ERROR
}

_CHARSET = 'utf-8'
_LOGFILE_FORMAT = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'
_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

_LOG_COLORS = {
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'purple',
    'CRITICAL': 'red',
}

_DISABLE_THIRD_LIST = [ 
    'requests', 
    'chardet.charsetprober'
]


class ColorLog:
    '''
    颜色日志器
    '''

    def __init__(self, 
            log_dir=_LOG_DIR, app_logs=_APP_LOGS, 
            logfile_format=_LOGFILE_FORMAT, date_format=_DATE_FORMAT, log_colors=_LOG_COLORS, 
            rollday=1, backupdays=7, encoding=_CHARSET, debug=True, 
            thirdlist=_DISABLE_THIRD_LIST) :
        '''
        初始化日志器。
        [param] log_dir: 日志输出目录
        [param] app_logs: 应用运行日志的名称字典，格式如 { name: min_level, ... }
        [param] logfile_format: 输出日志文件的格式
        [param] date_format: 输出日志文件的时间格式
        [param] logcolors: 日志每个等级的颜色字典，格式如 { level: color, ... }
        [param] rollday: 日志滚动间隔（单位：天）
        [param] backupdays: 备份日志时长（单位：天）
        [param] encoding: 日志编码
        [param] debug: 是否打印 debug 日志
        [param] thirdlist: 禁用的第三方日志列表
        :return: None
        '''
        self._debug = debug
        if not os.path.exists(log_dir) : os.mkdir(log_dir)
        self._logger = logging.getLogger()              # 创建日志记录器
        self._logger.setLevel(logging.DEBUG)            # 设置默认日志记录器记录级别
        self._init_handler(log_dir, app_logs, logfile_format, date_format, log_colors, rollday, backupdays, encoding)
        self._disable_third_logs(thirdlist)


    def _init_handler(self, log_dir, app_logs, logfile_format, date_format, log_colors, rollday, backupdays, encoding) :
        '''
        初始化日志处理器
        '''
        # 控制台日志
        console_handler = self._create_console_handler()
        self._set_console_formatter(console_handler, logfile_format, date_format, log_colors)
        console_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(console_handler)

        # 文件日志
        for logname, level in app_logs.items() :
            logpath = '%s/%s' % (log_dir, logname)
            logfile_handler = self._create_logfile_handler(logpath, rollday, backupdays, encoding)  # 创建日志文件
            self._set_logfile_formatter(logfile_handler, logfile_format, date_format)  # 设置日志格式
            logfile_handler.setLevel(level)
            self._logger.addHandler(logfile_handler)


    def _create_console_handler(self):
        '''
        创建控制台日志处理器
        '''
        console_handler = colorlog.StreamHandler()
        return console_handler


    def _set_console_formatter(self, console_handler, logfile_format, date_format, log_colors):
        '''
        设置控制台日志处理器的日志输出格式
        '''
        console_format = '%(log_color)s' + logfile_format
        formatter = colorlog.ColoredFormatter(console_format, datefmt=date_format, log_colors=log_colors)
        console_handler.setFormatter(formatter)


    def _create_logfile_handler(self, logpath, rollday, backupdays, encoding):
        '''
        创建文件日志处理器
        '''
        logfile_handler = TimedRotatingFileHandler(
            filename=logpath, 
            when="MIDNIGHT", 
            interval=rollday, 
            backupCount=backupdays, 
            encoding=encoding
        )
        return logfile_handler


    def _set_logfile_formatter(self, logfile_handler, logfile_format, date_format):
        '''
        设置文件日志处理器的日志输出格式
        '''
        formatter = logging.Formatter(logfile_format, datefmt=date_format)
        logfile_handler.setFormatter(formatter)


    def _disable_third_logs(self, thirdlist) :
        '''
        禁用第三方日志
        '''
        for third in thirdlist :
            logging.getLogger(third).setLevel(logging.FATAL)


    def debug(self, message) :
        '''
        打印调试信息
        [param] message: 日志信息
        :return: None
        '''
        if self._debug :
            self._logger.debug(message)


    def info(self, message) :
        '''
        打印正常信息
        [param] message: 日志信息
        :return: None
        '''
        self._logger.info(message)


    def warn(self, message) :
        '''
        打印警告信息
        [param] message: 日志信息
        :return: None
        '''
        self._logger.warning(message)


    def error(self, message) :
        '''
        打印异常信息和异常堆栈
        [param] message: 日志信息
        :return: None
        '''
        self._logger.error(message)
        if sys.exc_info()[0] is not None :
            self._logger.error(traceback.format_exc())


    def critical(self, message):
        '''
        打印严重信息和异常堆栈
        [param] message: 日志信息
        :return: None
        '''
        self._logger.critical(message)
        if sys.exc_info()[0] is not None :
            self._logger.critical(traceback.format_exc())



log = ColorLog()


