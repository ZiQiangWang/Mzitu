# -*- coding: utf-8 -*-
# @Date    : 2016-11-19 22:39:35
# @Author  : wangziqiang

import requests
import time
import random
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class wrequest(object):
    """增加多个User-Agent和代理防止反爬虫"""
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        self.proxy_list = [
            "223.68.1.38:8000",
            "124.88.67.24:843",
            "124.133.230.254:80",
            "220.248.229.45:3128",
            "116.242.227.201:3128",
            "121.193.143.249:80",
            "60.191.160.20:3128",
            "124.88.67.31:843",
            "61.185.137.126:3128",
            "218.67.126.15:3128",
            "122.226.152.2:3128",
            "115.159.185.186:8088",
            "1.82.216.135:80",
            "122.225.49.142:8080"
            ]

    def request_get(self, url, timeout=10, proxy=None, retry=6):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA}
        if not proxy:
            try:
                return requests.get(url,headers = headers,timeout=timeout)
            except Exception as e:
                print u"错误信息：" , e.message
                if retry>0:
                    print u"访问出错，10s后再次尝试。"+u"剩余尝试次数："+str(retry)+"。"
                    time.sleep(10)
                    return self.request_get(url,headers,timeout,retry-1)
                else:
                    proxy = {'http': random.choice(self.proxy_list)}
                    print u"开始使用代理", str(proxy)
                    timeout.sleep(10)
                    return self.request_get(url,timeout,proxy)
        else:
            try:
                return requests.get(url,headers = headers,proxies=proxy,timeout=timeout)
            except Exception as e:
                if retry>0:
                    print u"正在更换代理"
                    while True:
                        p = random.choice(self.proxy_list)
                        if p != proxy['http']:
                            proxy['http']=p
                            break
                    print u"新的代理为："+str(proxy)
                    time.sleep(10)
                    return self.request_get(url,timeout,proxy,retry-1)
                else:
                    print u"代理不可用！取消代理！"
                    return self.request_get(url,3)

wrequest_get = wrequest() ##实例化


