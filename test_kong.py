#!/usr/bin/python3
# -*- coding: utf-8
"""
@author: lanlmeng@qq.com
@file: test_kong.py
@time: 2020/2/21 18:17
@desc: 测试kong插件验证数据
"""
import base64
import datetime
import hashlib
import json
import hmac
import threading

import requests


def test_hmac_authentication():
    # 创建消费者对应HMAC插件时的用户名和秘钥
    hmac_username = "test_hmac"
    hmac_secret = "test_hmac_secret123"

    url = "https//example.com/v1/test_kong"

    # 请求头
    # 注意，请求头的时间格式必须是GMT时间格式
    request_headers = {
        "Authorization": "",
        "Digest": "",
        "Date": datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }

    # 请求体
    request_body = {
        "data": {"test": "hmac"}
    }

    # 生成Digest
    #  body="A small body"
    #  digest=SHA-256(body)
    #  base64_digest=base64(digest)
    #  Digest: SHA-256=<base64_digest>
    base64_digest = base64.b64encode(hashlib.sha256(json.dumps(request_body).encode('utf-8')).digest()).decode('utf-8')
    request_headers['Digest'] = "SHA-256={}".format(base64_digest)

    # 生成签名
    # signing_string = "date: Thu, 22 Jun 2017 17:15:21 GMT\nGET /requests HTTP/1.1"
    # digest = HMAC - SHA256( < signing_string >, "secret")
    # base64_digest = base64( < digest >)
    # 签名字符串构造
    # 如果参数不是request-line，则名字用小写，然后跟":"和一个空格" "，
    # 如果参数是request-line，则追加http请求行【GET /requests HTTP/1.1】
    # 中间用换行符"\n"将所有的参数连接起来。

    # 按照上述规则拼接字符串
    sign_string = "date: {}\ndigest: {}".format(request_headers['Date'], request_headers['Digest'])


    # 开始签名
    sign_digest = hmac.new(hmac_secret.encode("utf-8"), sign_string.encode('utf-8'), digestmod='sha256').digest()
    sign_base64_digest = base64.b64encode(sign_digest).decode('utf-8')

    # 构建Authorization参数 具体信息 https://docs.konghq.com/hub/kong-inc/hmac-auth/#signature-authentication-scheme
    authorization = 'hmac username="{}", algorithm="hmac-sha256", headers="date digest", signature="{}"'.format(
        hmac_username, sign_base64_digest)

    request_headers['Authorization'] = authorization
    resp = requests.post(url, headers=request_headers, json=request_body)
    print(request_headers)
    print(resp.status_code)
    print(resp.json())




def test_rate_limiting():
    url = "http://example.com/v1/test_kong"

    def _request(idx):
        print("request {} start by : {}".format(idx, datetime.datetime.now()))
        print("request {} result >>>".format(idx))
        resp = requests.get(url)
        print("request {} status_code {} ".format(idx, resp.status_code))
        print("request {} json {} ".format(idx, resp.json()))
        print("request {} result <<<".format(idx))
        print("request {} end by : {}".format(idx, datetime.datetime.now()))

    for i in range(0, 8):
        t = threading.Thread(target=_request, args=(i,))
        t.start()


if __name__ == "__main__":
    test_hmac_authentication()
