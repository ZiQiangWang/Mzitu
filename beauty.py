# -*- coding: utf-8 -*-
# @Date    : 2016-11-19 15:12:36
# @Author  : wangziqiang

import requests
from bs4 import BeautifulSoup
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

url = "http://www.mzitu.com/all"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}


PATH_IMAGE = 'images'

class Mzitu(object):
    """用来抓取网站www.mzitu.com的图片"""
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}

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
