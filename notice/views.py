from django.shortcuts import render
from django.template import loader
# Create your views here.
from notice.models import Notice
from notice.models import NoticeType

from django.http import HttpResponse, Http404, HttpResponseRedirect


def noticeList(request):
    # 从模型中获取数据
    notice_list = Notice.objects.order_by("notice_type")
    # 加载模板
    # 定义传输数据，是一个map
    context = {'notice_list': notice_list}

    # 将类型转为字符串
    for notice in notice_list:
        notice.notice_type = NoticeType[notice.notice_type][1]

    # return HttpResponse(template.render(context))
    return render(request, 'noticelist.html', context)


def noticedetail(request, notice_id):
    try:
        # 查找相关id的notice
        notice = Notice.objects.get(pk=notice_id)
    except notice.DoesNotExist:
        raise Http404("通知不存在！")

    return render(request, 'notice.html', {'notice': notice})


def studyline(request):
    return render(request,'studyline.html')


def index(request):
    return render(request, 'index.html')
