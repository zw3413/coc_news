from ffmpy3 import FFmpeg
import os
from news.video.ali_mp3 import transferMp3ToText

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import datetime

from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        handle_uploaded_file(request.FILES['file'])

        changeMp3SampleRate()
        result = listenByAli()
        srt = convertToSrt(result)

        if srt ==False :
            return HttpResponse('false', content_type="application/json,charset=utf-8")

        srtPath='/file/mp3/result.srt'
        srtFile=open(srtPath,'w+')
        srtFile.write(srt)
        srtLink='http://cloudbed.cn/file/mp3/result.srt'
        return HttpResponse(srtLink, content_type="application/json,charset=utf-8")


def convertTimeFormat(timestamp):
        return '0'+str(datetime.timedelta(milliseconds=timestamp))[0:11]

# 3
# 00:00:39,770 --> 00:00:41,880
# 在经历了一场人生巨变之后
# When I was lying there in the VA hospital ...


def convertToSrt(result):
    try:
        from news.coc_news_translate import translate_by_ali
        # print(result)
        sentences = result['Sentences']
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if(sentences[j]['BeginTime'] < sentences[j]['BeginTime']):
                    temp = sentences[j]['Begintime']
                    sentences[j]['BeginTime'] = sentences[i]['BeginTime']
                    sentences[i]['BeginTime'] = temp
                    j = j+1
                i = i+1

        sn = 1
        line = ''
        for i in range(len(sentences)):
            sentence=sentences[i]
            line = line + str(sn) + '\n'
            line = line + convertTimeFormat(sentence['BeginTime']) + \
                ' --> ' + convertTimeFormat(sentence['EndTime']) + '\n'
            line = line + translate_by_ali(sentence['Text']) + ' \n'
            line = line + sentence['Text'] + ' \n'
            line = line + '\n'
            sn = sn+1
        
        return line
    except:
        return False    


def handle_uploaded_file(f):
    tempMp3Path = '/file/mp3/sound.mp3'
    with open(tempMp3Path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# 将mp3码率转换为16k，达到ali ai的要求


def changeMp3SampleRate():
    sourcePath = '/file/mp3/sound.mp3'
    targetPath = '/file/mp3/temp.mp3'
    cmd = 'ffmpeg -y -i '+sourcePath+' -ar 16000 -ac 1 '+targetPath
    os.system(cmd)
    os.rename(targetPath, sourcePath)
    return True


# 调用ali ai接口，进行语音识别
def listenByAli():
    fileLink = 'http://www.cloudbed.cn/file/mp3/sound.mp3'
    listenedResult = transferMp3ToText(fileLink)
    # print(listenedResult)
    return listenedResult
