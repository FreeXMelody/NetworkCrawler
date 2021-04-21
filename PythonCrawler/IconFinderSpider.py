import requests
import re

import os
import sys

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

    ptn = re.compile('https://cdn(\d).iconfinder.com/data/icons/(.*?).png')
    link_match = re.search(ptn,html) # 此处使用search.不需要从字符串开头开始搜索
    return link_match.group(0)

    # <img src="https://cdn(\d).iconfinder.com/data/icons/(.*?).png" 1st
    
def saveToLocal(ImgUrl,path):
    fileName = ImgUrl.split("/")[-1]
    # 路径修正
    if path[-1] != '\\':
        path += '\\'
    fullPath = path + fileName
    try:
        # 检查 保存图片的目录 是否存在
        if not os.path.exists(path):
            os.mkdir(path)
            print("📁 检测目录不存在，已建立新目录")
        # 检查图片是否存在 不存在则爬取图片
        if not os.path.exists(fullPath):
            r = requests.get(ImgUrl)
            with open(fullPath,'wb') as f:
                f.write(r.content) # 写入所爬取图片的二进制数据
                f.close()
                print("图片已保存,文件名 %s" %fileName)
        else:
            print("文件已存在 🔒")
    except Exception as e:
        print(repr(e))
        print("爬取失败")

def downloadAll(aurl,apath):
    allLinks = ParserLinks(aurl)     # 获取所有子连接
    linksCount = len(allLinks)
    for i in range(0,linksCount):
        print("共%d个,第%d个" %(linksCount,i+1))
        imgUrl = getImgLink(allLinks[i])
        saveToLocal(imgUrl,apath)

def main():
    url = str(sys.argv[1])
    path = str(sys.argv[2])
    downloadAll(url,path)
    yesOrNo = input("✔️ 爬取完成啦，是否打开目录查看？(y) \n")
    if yesOrNo == "y":
        os.startfile(path)
    else:
        sys.exit

main()