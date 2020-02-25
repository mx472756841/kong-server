# -*- coding: utf-8 -*-
import importlib
import logging
import os
import signal
import time

import tornado.ioloop
import tornado.web
from tornado import httpserver, ioloop
from tornado.escape import native_str
from tornado.options import options, define

import settings

logger = logging.getLogger(__name__)

define("port", default=settings.PORT, help=u"run on given port", type=int)
define("host", default=settings.HOST, help=u"run on given host", type=str)

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1


class MyApplication(tornado.web.Application):
    """
    自定义Application
    添加redis
    添加db
    """

    def __init__(self, default_host=None, transforms=None,
                 **app_settings):
        handlers = self._import_handlers()
        default_settings = {
            "cookie_secret": 'aX0cSsEue2Q1WaNa3u2vtsq8cMS2knhiWd78wSS1sop0=',
            "xsrf_cookies": False
        }
        default_settings.update(app_settings)
        super(MyApplication, self).__init__(handlers, default_host, transforms, **default_settings)

    def _import_handlers(self):
        """
        动态导入tornado的处理类
        :param app:
        :return:
        """
        handlers = []
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        files = os.walk(os.sep.join([curr_dir, "handlers"]))
        for root, paths, fs in files:
            if "urls.py" in fs:
                module_name = root.split(os.sep)[-1]
                module = importlib.import_module("handlers." + module_name + ".urls")
                urls = getattr(module, 'urls', None)
                if urls:
                    handlers.extend(urls)
        return handlers


def sig_handler(sig, frame):
    logger.warning('caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logger.info('stopping http server')
    server.stop()
    logger.info('will shutdown in %s seconds...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop():
        now = time.time()
        if hasattr(io_loop, "_callbacks"):
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()
                logger.info('shutdown')
        else:
            io_loop.stop()
            logger.info('shutdown')

    stop_loop()


def io_loop_start():
    global server
    # 启动进程
    app = MyApplication()
    server = httpserver.HTTPServer(app, xheaders=True)
    logger.info('server is running on %s:%s' % (options.host, options.port))
    server.listen(options.port, options.host)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)


def main():
    # 重新设置一下日志级别，默认情况下，tornado 是 info
    # py2 下 options.logging 不能是 Unicode
    options.logging = native_str(settings.LOGGING_LEVEL)
    # parse_command_line 的时候将 logging 的根级别设置为 info
    options.parse_command_line()
    # 绑定服务端web监听端口
    io_loop_start()
    # 启动事件循环
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
