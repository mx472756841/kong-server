#!/usr/bin/python3
# -*- coding: utf-8
"""
@author: lanlmeng@qq.com
@file: urls.py
@time: 2020/2/21 18:17
"""

from tornado.web import url
import handlers.test_kong.views as vw

urls = [
    url(r"^/v1/test_kong", vw.TestKong),
]
