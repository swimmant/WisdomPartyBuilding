from django.conf.urls import url

from notice import views

urlpatterns = [
    #"职位列表"

    url(r"^noticelist/",views.noticeList,name="noticeList"),
    url(r'^notice/(?P<notice_id>\d+)/$',views.noticedetail,name="noticedetail"),

    #设置首页调转到通知页面
    url(r'^$',views.noticeList,name="name"),
    url(r'^index/',views.index,name="index"),
    url(r'^studyline/',views.studyline,name="studyline")
]