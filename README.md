# Mzitu
爬虫，抓取妹子图网站的图片

妹子图网址：http://www.mzitu.com/all

基本上是按照这个教程来的
http://cuiqingcai.com/3314.html

第三方库：
requests获取网页源码和图片下载
BeautifulSoup4解析
pymongo爬取过的网址存储，避免下次重新来一次
gevent协程，增加爬取效率
