import logging
import os

from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
# Create your views here.
from studyfiles.models import studyFiles

from django.views import View
# 快速创建视图
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from studyfiles.models import fileType
fileTypeIndex = {"活动":0,"会议":1,"通告":2,"学习":3}
# fileType = [(u'活动', u"活动"), (u'会议', u"会议"), (u'通告', u"通告"), (u"学习", u"学习")]

def get(request):  # 定义类试图的get方法
    logging.info("获取文件list请求")

    # 从模型中获取数据
    file_list = studyFiles.objects.order_by("file_type")

    typelist = []
    for type in fileType:
        typelist.append(type[1])


    # 加载模板
    # 定义传输数据，是一个map
    context = {'file_list': file_list,"filetype":typelist}

    # # 将类型转为字符串
    # for file in file_list:
    #     file_list.file_type = fileType[file.file_type][1]

    # return HttpResponse(template.render(context))
    return render(request, 'studyfile.html', context)


def upload(request):  # 定义类试图的post方法
    logging.info("接受post请求")
    file_type= request.POST.get('filetype', '')
    print(request)
    file = request.FILES
    print(file)
    myfile = request.FILES.get("myfile", '')  # 将请求上传的文件赋值给myfile
    # if file_record == '':
    #     return HttpResponse('文件上传信息不能为空')
    if myfile == '':
        return HttpResponse('未选择上传的文件,请重新选择后上传')
    file_name = myfile.name
    # 检测文件是否存在，如果存在就自动变更名称
    file_name = file_check(file_name)
    with open("static/file/" + file_name, "wb") as fp:  # 打开static目录下的文件，文件用myfile名称，并设置简称为fp
        for chunk in myfile.chunks():  # 遍历myfile的数据流
            fp.write(chunk)  # 将数据流写入到fp文件中
    # TODO：存储数据，并返回上一页
    file = studyFiles()
    print(request.POST)
    file.file_name = file_name
    file.file_type = fileTypeIndex[file_type]
    file.creator = request.user
    file.file_http = 'http://{}/static/file/{}'.format(request.META.get('HTTP_HOST'), file_name)
    file.save()

    return HttpResponseRedirect('/studyfile/')


def file_check(file_name):
    temp_file_name = file_name
    i = 1
    while i:
        print(temp_file_name)
        print(os.path.exists("static/file/" + temp_file_name))
        if os.path.exists("static/file/" + temp_file_name):
            name, suffix = file_name.split('.')
            name += '(' + str(i) + ')'
            temp_file_name = name + '.' + suffix
            i = i + 1
        else:
            return temp_file_name
