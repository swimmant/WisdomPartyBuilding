from django.conf.urls import url

from studyfiles import views

urlpatterns = [
    #"学习文件列表"

    url(r"^studyfile/",views.get,name="fileList"),
    url(r"^upload/",views.upload,name="up_load"),

]