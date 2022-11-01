import os
import requests
import json
import lxml.html
import re
import time
import random

delay = random.randint(60, 100)
print(delay)
time.sleep(delay)
User_Agent = 'Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/201101 Mobile Safari/537.36 MMWEBID/9229 MicroMessenger/7.0.21.1847(0x27001545) Process/toolsmp WeChat/arm64 Weixin GPVersion/1 NetType/4G Language/zh_CN ABI/arm64'

#signIn = {'username': os.environ["USERNAME"], #学号
          'password': os.environ["PASSWORD"]} #登陆密码

headers = {
    'User-Agent': User_Agent,
}

conn = requests.Session()
signInResponse= conn.post(
    url="https://app.upc.edu.cn/uc/wap/login/check",
    headers=headers,
    data= signIn, 
    timeout=10
)

historyResponse = conn.get(
    url="https://app.upc.edu.cn/ncov/wap/default/index?from=history",
    headers=headers,
    data={'from': 'history'},
    timeout=10
)
historyResponse.encoding = "UTF-8"

html = lxml.html.fromstring(historyResponse.text)
JS = html.xpath('/html/body/script[@type="text/javascript"]')
JStr = JS[0].text
default = re.search('var def = {.*};',JStr).group()
oldInfo = re.search('oldInfo: {.*},',JStr).group()

firstParam = re.search('sfzgsxsx: .,',JStr).group()
firstParam = '"' + firstParam.replace(':','":')
secondParam = re.search('sfzhbsxsx: .,',JStr).group()
secondParam = '"' +  secondParam.replace(':','":')
lastParam = re.search('szgjcs: \'(.*)\'',JStr).group()
lastParam = lastParam.replace('szgjcs: \'','').rstrip('\'')

newInfo = oldInfo
newInfo = newInfo.replace('oldInfo: {','{' + firstParam + secondParam).rstrip(',')

defaultStrip = default.replace('var def = ','').rstrip(';')
defdic = json.loads(defaultStrip)

dic = json.loads(newInfo)
dic['ismoved'] = '0'
for j in ["date","created","id","gwszdd","sfyqjzgc","jrsfqzys","jrsfqzfy","sfzx"]:
    dic[j] = defdic[j]
dic['szgjcs'] = lastParam

saveResponse = conn.post(
    url="https://app.upc.edu.cn/ncov/wap/default/save",
    headers=headers,
    data = dic,
    timeout=10
)

saveJson = json.loads(saveResponse.text)
print(saveJson['m'])
