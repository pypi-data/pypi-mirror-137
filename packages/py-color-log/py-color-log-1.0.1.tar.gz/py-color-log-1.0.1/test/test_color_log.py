#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
# ----------------------------------------------------------------------
# 把父级目录（项目根目录）添加到工作路径，以便在终端也可以执行单元测试
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import unittest
from src.color_log import log


class TestScenes(unittest.TestCase):
    '''
    测试从文件读取视频识别人体的效果
    '''

    @classmethod
    def setUpClass(cls) :
        pass


    @classmethod
    def tearDownClass(cls) :
        pass

    def setUp(self) :
        pass


    def tearDown(self) :
        pass


    def test_color_log(self) :
        log.debug('这是 DEBUG 日志，白色')
        log.info('这是 INFO 日志，青绿')
        log.warn('这是 WARN 日志，黄色')
        log.error('这是 ERROR 日志，紫色')
        try :
            a = 1 / 0
        except :
            log.critical('这是 CRITICAL 日志，红色')
        
        

if __name__ == '__main__':
    unittest.main()
