# -*- coding: utf-8
"""
@author: lanlmeng@qq.com
@file: views.py
@time: 2020/2/21 18:17
"""
import logging

from tornado.escape import json_decode
from tornado.web import RequestHandler

logger = logging.getLogger('common')


class BaseRequestHandler(RequestHandler):
    def success(self, msg, data=None):
        """
        执行成功,code为200,msg信息为实际信息,data存在时,将data一并返回
        :param msg:
        :param data:
        :return:
        """
        result = {
            "code": 200,
            "message": msg
        }
        if data is not None:
            result['data'] = data
        self.finish(result)

    def fail(self, msg, code=400, data=None):
        result = {
            "code": int(code),
            "message": msg
        }
        if data is not None:
            result['data'] = data
        self.finish(result)


    def prepare(self):
        """
        重写prepare方法
        content-type为Application时，将内容解析到self.json_body
        :return:
        """
        super(BaseRequestHandler, self).prepare()
        self.json_body = {}
        self.referer = self.request.headers.get("Referer", "")
        if self.request.headers.get("Content-Type", "") == "application/json":
            # 前端传输类型是json的话，进行解析，后端使用json_body进行处理，因为tornado自带的数据解析不包含application/json类型
            body = self.request.body.decode("utf-8")
            if body:
                try:
                    body = json_decode(body)
                except:
                    body = {}
                self.json_body = body

