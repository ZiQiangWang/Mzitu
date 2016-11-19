# -*- coding: utf-8 -*-
# @Date    : 2016-11-19 15:12:36
# @Author  : wangziqiang

import requests
from bs4 import BeautifulSoup
import os
import sys
import re
import random

reload(sys)
sys.setdefaultencoding('utf8')

url = "http://www.mzitu.com/all"

PATH_IMAGE = 'images'

class Mzitu(object):
    """用来抓取网站www.mzitu.com的图片"""
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

    def save(self,img_url, path):
        """传入图片的url，保存到对应位置,path是图片保存的路径"""
        img = self.request_get(img_url, args='content')
        with open(path+'/'+img_url[-9:],'wb') as f:
            f.write(img)
            f.close()

    def request_get(self, url, args='text'):
        """根据url返回网站内容
            args可以填text或content
        """
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA}
        rep = requests.get(url,headers = headers)
        if rep.status_code != 200:
            print  url+'访问失败'
            return None

        if args == 'text':
            return rep.text
        elif args == 'content':
            return rep.content
        else:
            return None

    def validate_name(self, name):
        """windows下文件夹非法命名校验"""
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_name = re.sub(rstr, "_", name)
        return new_name

    def get_images(self,url):
        rep = self.request_get(url)
        soup = BeautifulSoup(rep, 'html.parser')
        years = soup.find('div',class_='all').find_all('div',class_='year')

        for y in years:
            year_path = os.path.join(PATH_IMAGE,y.text).replace("\\","/")
            if not os.path.exists(year_path):
                os.mkdir(year_path)

            year_pic = y.next_sibling
            months = year_pic.find_all('p', class_='month')
            for m in months:
                month_path = os.path.join(year_path,m.find('em').text).replace("\\","/")
                if not os.path.exists(month_path):
                    os.mkdir(month_path)

                month_pic = m.next_sibling.find_all('a')
                for mp in month_pic:
                    title = mp.text
                    page_path = os.path.join(month_path,title).replace("\\","/")
                    if not os.path.exists(page_path):
                        try:
                            os.mkdir(page_path)
                        except Exception as e:
                            title = validate_name(title)
                            page_path = os.path.join(month_path,title).replace("\\","/")
                            os.mkdir(page_path)

                    href = mp['href']
                    print "开始获取《"+title+"》"
                    self.get_pages(href,page_path)

    def get_pages(self,url,path):
        """获取每一个专辑的图片"""
        page  = self.request_get(url)
        s = BeautifulSoup(page, 'html.parser')
        max_index = s.find('div',class_='pagenavi').find_all('span')[6].text

        for x in xrange(1,int(max_index)+1):
            page_url = url+'/'+str(x)
            image_html = self.request_get(page_url)
            img_soup = BeautifulSoup(image_html, 'html.parser')
            img_url = img_soup.find('div', class_='main-image').find('img')['src']

            self.save(img_url,path)


m = Mzitu()
m.get_images(url)
