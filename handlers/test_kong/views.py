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


class TestKong(BaseRequestHandler):

    async def get(self):
        return self.success("test kong get success")

    async def post(self, *args, **kwargs):
        return self.success("test kong post success")

    async def delete(self):
        return self.success("test kong delete success")

    async def put(self, *args, **kwargs):
        return self.success("test kong put success")