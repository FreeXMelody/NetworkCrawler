import requests
import os
import re

import json

def GetGroupLink(imgGroupID):
    # 提供图片组ID
    lastIDNumber = imgGroupID[-1]
    ImgLink = "https://i.gtimg.cn/club/item/parcel/" + lastIDNumber + "/" + imgGroupID + "_android.json?mType=VIP_emosm"
    return ImgLink


def GetHtml(url):        
    # 获取json
    headers = {
        'User-agent':'Mozilla/5.0'
    }
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    r.raise_for_status
    return r.text

# 属于json复杂字符串的解析
def parserJSON(html):
    data = json.loads(html)
    return data

def getImgID(jsonData):
    idDict = []
    imgsData = jsonData['imgs']
    imgCount = len(imgsData)
    for i in range(0,imgCount):
        idDict.append(imgsData[i]['id'])
    return idDict

####  抓取图片  ####

def getImgLink(imgID):
    pageIndex = str(imgID[0])+str(imgID[1])
    link = "https://i.gtimg.cn/club/item/parcel/item/" + pageIndex +"/" + imgID +"/" + "126x126.png"
    return link

def saveToLocal(ImgUrl,path):
    fileName = ImgUrl.split("/")[-2] + ".png"
    print("====  Got file name:  " + fileName + "   ====")
    fullPath = path + fileName
    try:
        # 检查目录是否存在
        if not os.path.exists(path):
            os.mkdir(path)
            print("目录不存在，已建立新目录")

        if not os.path.exists(fullPath):
            r = requests.get(ImgUrl)
            with open(fullPath,'wb') as f:
                f.write(r.content) # 写入数据
                f.close()
                print("图片已保存,文件名 %s" %fileName)
        else:
            print("文件已存在")
    except Exception as e:
        print(repr(e))
        print("爬取失败")


def main():
    link = GetGroupLink("204096")   # 更改图片组 ID 即可

    html = GetHtml(link)
    jsonData = parserJSON(html) # dict
    IDs = getImgID(jsonData)
    print(IDs[0])
    getImgLink(IDs[0])

    for i in IDs:
        imgUrl = getImgLink(i)
        saveToLocal(imgUrl,'F:/SWEETIE BUNNY/')


main()

