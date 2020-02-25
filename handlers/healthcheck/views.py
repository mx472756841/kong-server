#!/usr/bin/python3
# -*- coding: utf-8
"""
@author: lanlmeng@qq.com
@file: views.py
@time: 2020/2/21 18:17
"""
import logging

from common.tornado.web import BaseRequestHandler

logger = logging.getLogger('common')


class HealthCheck(BaseRequestHandler):

    async def head(self):
        """
        用于Kong检查服务是否可用
        :return:
        """
        return self.success("ok")

    async def options(self):
        return self.success("ok")

    async def get(self):
        return self.success("ok")