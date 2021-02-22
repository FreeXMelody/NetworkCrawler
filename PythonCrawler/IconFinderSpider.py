import requests
import re

import os

# 初始化，获取网页源码
def init(url):
    headers = {
        'User-agent':'Mozilla/5.0'
    }
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    r.raise_for_status
    return r.text

# 获取图片组链接
def getLinks(html):
    # 链接构成 https://www.iconfinder.com/icons/   ID   / 名称
    pt = re.compile('data-asset-id="(\d+)"')
    LinkList1 = re.findall(pt,html)
    return LinkList1

# main
def ParserLinks(url):
   html = init(url)
   name = []

   parseredLinks = []
   allLinks = []

   links = getLinks(html)
   # 获取图片名称
   for i in links:
       ptn = re.compile('href="/icons/' + i + '/(.*?)"')
       res = "".join(re.findall(ptn, html)) # 删除name左右括号 
       name.append(res)
    
   for index in range(0,len(links)):
        # namePlus = eval(str(name[index])) # 可用于去除name两端引号
        parseredLinks.append('https://www.iconfinder.com/icons/' + str(links[index]) + "/" + str(name[index]))

   for link in parseredLinks:
        allLinks.append(link)
   return allLinks

# 获取图片链接
def getImgLink(link):
    r = requests.get(link)
    r.encoding = r.apparent_encoding
    r.raise_for_status
    html = r.text

    # soup = bs(html,'html.parser') 

    ptn = re.compile('https://cdn(\d).iconfinder.com/data/icons/(.*?).png')
    link_match = re.search(ptn,html) # 应该用search...正则写的是对的，在re的理解上还不够啊~。。 search不需要从字符串开头开始搜索
    print(link_match.group(0))
    return link_match.group(0)

    # <img src="https://cdn2.iconfinder.com/data/icons/(.*?).png" 一般是第一个
    
def saveToLocal(ImgUrl):
    path = "F:/DevelopmentAndMarketingIcon/"
    fileName = ImgUrl.split("/")[-1]
    print("====  Got file name:  " + fileName + "   ====")
    fullPath = path + fileName
    try:
        # 检查 保存图片的目录 是否存在
        if not os.path.exists(path):
            os.mkdir(path)
            print("目录不存在，已建立新目录")
        # 检查图片是否存在 不存在则爬取图片
        if not os.path.exists(fullPath):
            r = requests.get(imgUrl)
            with open(fullPath,'wb') as f:
                f.write(r.content) # 写入所爬取图片的二进制数据
                f.close()
                print("图片已保存,文件名%s" %fileName)
        else:
            print("文件已存在")
    except:
        print("爬取失败")



allLinks = ParserLinks("https://www.iconfinder.com/iconsets/webina-seo-development-and-marketing")     # 获取所有子连接
linksCount = len(allLinks)
for i in range(0,linksCount):
    print("共%d个,第%d个" %(linksCount,i+1))
    imgUrl = getImgLink(allLinks[i])
    saveToLocal(imgUrl)


# print(allLinks[0])
# imgUrl = getImgLink(allLinks[0])
# saveToLocal(imgUrl)
