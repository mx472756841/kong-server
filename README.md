# kong-server
kong网关后端服务接口配置

## virtualenv部署启动

1. virtualenv -p python3.6 venv
2. . venv/bin/activate
3. pip install -r requirements.txt
4. python server.py --port=10020

## 文件说明

etc/kong_proxy.conf 使用nginx配置kong的具体信息

test_kong.py 测试kong相关插件的脚本文件
