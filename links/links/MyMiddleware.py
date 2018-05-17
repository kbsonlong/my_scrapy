#coding: utf-8

import json ##处理json的包
import redis #Python操作redis的包
import random #随机选择
from .useragent import agents #导入前面的
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #UserAegent中间件
from scrapy.downloadermiddlewares.retry import RetryMiddleware #重试中间件


class UserAgentmiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent