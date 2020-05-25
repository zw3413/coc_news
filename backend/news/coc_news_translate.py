#!/usr/bin/env python
#coding=utf-8
import json
import requests
from news.coc_news_util import *

#目前可以使用的翻译方法有：
# translate_by_ali      yes,支持text和html
# translate_by_google   yes,支持text和html
# translate_by_youdao   频繁调用会被封,仅支持text
# translate_by_bing     需要申请azure的试用key

googleEngine='http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh&q='
bingEngine='http://api.microsofttranslator.com/v2/Http.svc/Translate?appId=AFC76A66CF4F434ED080D245C30CF1E71C22959C&from=&to=en&text='
youdaoEngine='http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i='

def translate_by_google(enText):
    def resolveGoogle(res):
        j={}
        try:
            j=json.loads(res)
        except:
            print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            print(res)
        else:
            j['sentences']=[]
        result=''
        if len(j['sentences'])>0:
            for sentence in j['sentences']:
                result=result+'\n'+sentence['trans']
            result=result[1:len(result)]    
        return result
    engine=googleEngine
    enText_list=split_text(enText,5000)
    result=''
    for t in enText_list:
        url=engine+t
        headers={'user-agent': 'Mozilla/5.0'}
        res=requests.get(url,headers=headers)
        res.encoding="UTF-8"
        result= result+resolveGoogle(res.text)
    return result

def translate_by_bing(enText):
    engine=bingEngine
    url=engine+enText
    headers={'user-agent': 'Mozilla/5.0'}
    res=requests.get(url,headers=headers)
    res.encoding="UTF-8"
    result=res.text
    return result

def translate_by_youdao(enText):
    def resolveYoudao(result):
        j=json.loads(result)
        if j['errorCode']==0:
            result = j['translateResult'][0][0]['tgt']
        else:
            result = None
        return result
    engine=youdaoEngine
    url=engine+enText
    headers={'user-agent': 'Mozilla/5.0'}
    res=requests.get(url,headers=headers)
    res.encoding="UTF-8"
    result=resolveYoudao(res.text)
    return result

def translate_by_ali(enText):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkalimt.request.v20181012.TranslateGeneralRequest import TranslateGeneralRequest
    
    accessKeyId='LTAI4GD3uZc5eGXHtustt68w'
    accessSecret='EicjId1cYJFd3HXAyhXwumWFpfXzBa'
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    request = TranslateGeneralRequest()
    request.set_accept_format('json')

    request.set_FormatType("html")
    request.set_SourceLanguage("en")
    request.set_TargetLanguage("zh")
    request.set_SourceText(enText)
    request.set_Scene("general")

    response = client.do_action_with_exception(request)
    # python2:  print(response) 
    print(str(response, encoding='utf-8'))
    res=json.loads(response)
    result=''
    if(res['Code']=="200"):
        result=res['Data']['Translated'] 
    else:
        result=None
    return result

if(__name__=='__main__'):
    enText="<a>Hello, my dear.</a>"
    zhText=translate_by_ali(enText)
    print(zhText)