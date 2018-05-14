import requests
from urllib import parse
import execjs
import json
import io
import sys
import re
import time
import pandas as pd
import openpyxl
from app.main import global_values
from flask import request,jsonify

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')		#改变标准输出的默认编码
session = requests.Session()


s=''
Param = "全文检索:" + s  # 搜索关键字
Index = 1  # 第几页
Page = 20  # 每页几条
Order = "法院层级"  # 排序标准
Direction = "asc"  # asc正序 desc倒序



def get_guid():
    #获取guid参数
    js1 = '''
        function getGuid() {
            var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
            return guid;
        }
        var createGuid = function () {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        }
    '''
    ctx1 = execjs.compile(js1)
    guid = (ctx1.call("getGuid"))
    return guid

def get_number(guid):
    ###获取number
    codeUrl = "http://wenshu.court.gov.cn/ValiCode/GetCode"
    data = {
        'guid':guid
    }
    headers = {
        'Host':'wenshu.court.gov.cn',
        'Origin':'http://wenshu.court.gov.cn',
        'Referer':'http://wenshu.court.gov.cn/',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    req1 = session.post(codeUrl,data=data,headers=headers)
    number = req1.text
    return number

def get_vjkl5(guid,number):
    ####获取cookie中的vjkl5
    url1 = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number="+number+"&guid="+guid+"&conditions=searchWord+QWJS+++"+parse.quote(Param)
    Referer1 = url1
    headers1 = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Host":"wenshu.court.gov.cn",
        "Proxy-Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }
    req1 = session.get(url=url1,headers=headers1,timeout=10)
    try:
        vjkl5 = req1.cookies["vjkl5"]
        return vjkl5
    except:
        return get_vjkl5(guid,number)

def get_vl5x(vjkl5):
    #根据vjkl5获取参数vl5x
    js = ""
    fp1 = open('app/main/spider/sha1.js')
    js += fp1.read()
    fp1.close()
    fp2 = open('app/main/spider/md5.js')
    js += fp2.read()
    fp2.close()
    fp3 = open('app/main/spider/base64.js')
    js += fp3.read()
    fp3.close()
    fp4 = open('app/main/spider/vl5x.js')
    js += fp4.read()
    fp4.close()
    ctx2 = execjs.compile(js)
    vl5x = (ctx2.call('vl5x',vjkl5))
    return vl5x


def get_data(Param,Index,Page,Order,Direction):
    guid = get_guid()
    number = get_number(guid)
    vjkl5 = get_vjkl5(guid,number)
    vl5x = get_vl5x(vjkl5)

    content_s = []  # 裁判要旨段原文
    case_type_s = []  # 案件类型
    judge_date_s = []  # 裁判日期
    case_name_s = []  # 案件名称
    official_id_s = []  # 文书ID
    judge_process_s = []  # 审判程序
    case_id_s = []  # 案号
    court_name_s = []  # 法院名称


    url2 = "http://wenshu.court.gov.cn/List/ListContent"
    headers2 = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"wenshu.court.gov.cn",
        "Origin":"http://wenshu.court.gov.cn",
        "Proxy-Connection":"keep-alive",
        # "Referer":Referer1,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
    }
    data = {
        "Param":Param,
        "Index":Index,
        "Page":Page,
        "Order":Order,
        "Direction":Direction,
        "vl5x":vl5x,
        "number":number,
        "guid":guid
    }
    # req2 = session.post(url=url2,headers=headers2,params=data)
    # req2.encoding='utf-8'
    # r_json=req2.json()
    # pattern1 = re.compile('"裁判日期":"(.*?)"', re.S)
    # judge_date = re.findall(pattern1, r_json)
    # pattern2 = re.compile('"案号":"(.*?)"', re.S)
    # case_id = re.findall(pattern2, r_json)
    # pattern3 = re.compile('"案件名称":"(.*?)"', re.S)
    # case_name = re.findall(pattern3, r_json)
    # pattern4 = re.compile('"法院名称":"(.*?)"', re.S)
    # court_name = re.findall(pattern4, r_json)
    # pattern5 = re.compile('"审判程序":"(.*?)"', re.S)
    # judge_process = re.findall(pattern5, r_json)
    # pattern6 = re.compile('"案件类型":"(.*?)"', re.S)
    # case_type = re.findall(pattern6, r_json)
    # pattern7 = re.compile('"文书ID":"(.*?)"', re.S)
    # official_id = re.findall(pattern7, r_json)
    # pattern8 = re.compile('"裁判要旨段原文":"(.*?)"', re.S)
    # content = re.findall(pattern8, r_json)
    # content_s+=content      #裁判要旨段原文
    # case_type_s+=case_type    #案件类型
    # judge_date_s+=judge_date   #裁判日期
    # case_name_s+=case_name    #案件名称
    # official_id_s+=official_id  #文书ID
    # judge_process_s+=judge_process#审判程序
    # case_id_s+=case_id      #案号
    # court_name_s+=court_name   #法院名称
    #
    #
    # df = pd.DataFrame({
    #     '时间': judge_date_s,
    #     '案号': case_id_s,
    #     '案件名称': case_name_s,
    #     '法院名称': court_name_s,
    #     '案件类型': case_type_s,
    #     '审判程序': judge_process_s,
    #     '文书ID': official_id_s,
    #     '裁判要旨段原文': content_s
    # })
    # df.to_excel('G:\\result.xlsx')
    # print(df)
    req2 = session.post(url=url2, headers=headers2, params=data)
    return req2.json()


def run(key):
    s=key
    Param = "全文检索:" + s  # 搜索关键字
    Index = 1  # 第几页
    Page = 20  # 每页几条
    Order = "法院层级"  # 排序标准
    Direction = "asc"  # asc正序 desc倒序
    return get_data(Param, Index, Page, Order, Direction)

if __name__ == '__main__':
    s = '非法集资'
    # 搜索条件
    Param = "全文检索:" + s  # 搜索关键字
    Index = 1  # 第几页
    Page = 20  # 每页几条
    Order = "法院层级"  # 排序标准
    Direction = "asc"  # asc正序 desc倒序
    get_data(Param, Index, Page, Order, Direction)



