import re,os,random,datetime,math
from shutil import copyfile
import time,json,hashlib,base64
import httpx
from bs4 import BeautifulSoup
import urllib.parse

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()

def DSGet(q = "",b = None):
    if b:
        br = json.dumps(b)
    else:
        br = ""
    s = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
    t = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    c = md5("salt=" + s + "&t=" + t + "&r=" + r + "&b=" + br + "&q=" + q)
    return t + "," + r + "," + c

def GetUidPic(raw_data,uid,qid,nickname):
    style = "egenshin"
    url = "https://yuanshen.minigg.cn/generator/user_info?style=" + style + "&uid=" + uid + "&qid=" + qid + "&nickname=" + urllib.parse.quote(nickname) +"&quality=75"
    req = httpx.post(
        url = url,
        json = raw_data
    )
    return req.text

def GetInfo(Uid,ck,ServerID="cn_gf01"):
    if Uid[0] == '5':
        ServerID = "cn_qd01"
    try:
        req = httpx.get(
            url="https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/index?role_id=" + Uid + "&server=" + ServerID,
            headers={
                'DS': DSGet("role_id=" + Uid + "&server=" + ServerID),
                'x-rpc-app_version': "2.11.1",
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1',
                'x-rpc-client_type': '5',
                'Referer': 'https://webstatic.mihoyo.com/',
                "Cookie": ck})
        data = json.loads(req.text)
        return data
    except:
        print("访问失败，请重试！")

def GetMysInfo(mysid,ck):
    try:
        req = httpx.get(
            url="https://api-takumi-record.mihoyo.com/game_record/card/wapi/getGameRecordCard?uid=" + mysid,
            headers={
                'DS': DSGet("uid="+mysid),
                'x-rpc-app_version': "2.11.1",
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1',
                'x-rpc-client_type': '5',
                'Referer': 'https://webstatic.mihoyo.com/',
                "Cookie": ck})
        data = json.loads(req.text)
        return data
    except:
        im = "err，获取米游社信息失败，请重试！"
        print(im)
        return im

def GetWeaponInfo(name):
    req = httpx.get(
        url="https://genshin.minigg.cn/?weapons=" + name,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'Referer': 'https://genshin.minigg.cn/index.html'})
    soup = BeautifulSoup(req.text, "lxml")
    item = soup.select_one("pre").text
    data = json.loads(item)
    return data

def GetCharTalentsInfo(name):
    baseurl = "https://api.minigg.cn/talents?query="
    req = httpx.get(
        url = baseurl + name,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'Referer': 'https://genshin.minigg.cn/index.html'})
    data = jsonfy(req.text)
    return data

def GetCharInfo(name,mode = 0,level = None):
    str = ""
    if mode == 1:
        str = "&talents=1"
    elif mode == 2:
        str = "&constellations=1"
    
    baseurl = "https://genshin.minigg.cn/?characters="

    detailurl = "https://api.minigg.cn/characters?query="

    if level:
        req = httpx.get(url = detailurl + name + "&stats=" + level,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'Referer': 'https://genshin.minigg.cn/index.html'})
        data = jsonfy(req.text)
    else:
        req = httpx.get(
            url = baseurl + name + str,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'Referer': 'https://genshin.minigg.cn/index.html'})

        soup = BeautifulSoup(req.text, "lxml")
        item = soup.select_one("pre").text
        if item:
            data = json.loads(item)
        else:
            req = httpx.get(
                    url = detailurl + name + "&matchCategories=true",
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                        'Referer': 'https://genshin.minigg.cn/index.html'})
            data = req.text

    return data

def GetGenshinEvent(mode = "List"):
    if mode == "Calendar":
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        base_url = "https://api-takumi.mihoyo.com/event/bbs_activity_calendar/getActList?time={}&game_biz=ys_cn&page=1&tag_id=0".format(now_time)
    else:
        base_url = "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnn" + mode + "?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&level=55&uid=100000000"
    
    req = httpx.get(
        url = base_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'})
    data = json.loads(req.text)
    return data

def jsonfy(s:str)->object:
    #此函数将不带双引号的json的key标准化
    s = s.replace("stats: [Function (anonymous)]","")
    obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj