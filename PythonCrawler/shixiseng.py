# beautiful soup 参考文档 https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
# https://www.shixiseng.com/interns?page=1&keyword=python
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"
}

def detail_get(url):
    r = requests.get(url)
    soup = bs(r.text,'lxml')
    # 获取标题 内容 .text只取文字
    title = soup.title.text
    # 获取公司名
    company_name = soup.select('.con-job .com_intro .com-name')[0].text
    # 获取薪资
    job_money = soup.select('.job_money.cutom_font')[0].text.encode('utf-8')    # 重新编码
    # 替换值
    job_money = job_money.replace(b'\xee\x8c\xa8',b'0')
    job_money = job_money.replace(b'\xef\x81\xaa',b'1')
    job_money = job_money.replace(b'\xef\x97\x8b',b'2')
    job_money = job_money.replace(b'\xee\xa8\x80',b'3')
    job_money = job_money.replace(b'\xee\x97\xa5',b'4')
    job_money = job_money.replace(b'\xee\xac\xbf',b'5')
    job_money = job_money.replace(b'\xee\xa4\x83',b'8')

    job_money = job_money.decode() # 解码

    # 薪资显示为方框，网站有反爬虫机制，此处需要破解 ， 原理来自编码映射关系
    print(title + company_name + job_money + "   " +  url + '\n')

def crawler():
    # 获取前五页的信息
    for page in range(1,5):
        r = requests.get("https://www.shixiseng.com/interns?page={}&keyword=python".format(page),headers=headers)
        # 使用bs4库进行解析
        soup = bs(r.text,'lxml')
        offers = soup.select('.intern-wrap.intern-item') # 匹配所有包含主要信息的div标签
        # 再从其子元素下提取url
        for offer in offers:
            url = offer.select('.f-l.intern-detail__job p a')[0]['href']
            detail_get(url)


crawler()