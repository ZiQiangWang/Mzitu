# -*- coding: utf-8 -*-
# @Date    : 2016-11-19 15:12:36
# @Author  : wangziqiang

from bs4 import BeautifulSoup
import os
import sys
import re
from pymongo import MongoClient
from wrequest import wrequest_get
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

url = "http://www.mzitu.com/all"

PATH_IMAGE = 'images'

class Mzitu(object):
    """用来抓取网站www.mzitu.com的图片"""
    def __init__(self):
        client = MongoClient()
        db = client['spider']
        self.meizitu_collection = db['meizitu']

    def save(self,img_url, path):
        """传入图片的url，保存到对应位置,path是图片保存的路径"""
        img = wrequest_get.request_get(img_url).content
        with open(path+'/'+img_url[-9:],'wb') as f:
            f.write(img)
            f.close()

    def validate_name(self, name):
        """windows下文件夹非法命名校验"""
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_name = re.sub(rstr, "_", name)
        return new_name

    def get_images(self,url):
        rep = wrequest_get.request_get(url).text
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
                    if self.meizitu_collection.find_one({'主题页面': href}):
                        print u"已经爬过这个页面："+title
                    else:
                        print u"开始获取："+title
                        self.get_pages(href,title,page_path)

    def get_pages(self,url,title,path):
        """获取每一个专辑的图片"""
        page  = wrequest_get.request_get(url).text
        s = BeautifulSoup(page, 'html.parser')
        max_index = s.find('div',class_='pagenavi').find_all('span')[6].text

        img_urls = []
        for x in xrange(1,int(max_index)+1):
            page_url = url+'/'+str(x)
            image_html = wrequest_get.request_get(page_url).text
            img_soup = BeautifulSoup(image_html, 'html.parser')
            img_url = img_soup.find('div', class_='main-image').find('img')['src']
            img_urls.append(img_url)
            self.save(img_url,path)

        post = {
            '标题': title,
            '主题页面': url,
            '图片地址': img_urls,
            '获取时间': datetime.datetime.now()
        }
        self.meizitu_collection.save(post)
        print u"保存数据成功"




m = Mzitu()
m.get_images(url)
