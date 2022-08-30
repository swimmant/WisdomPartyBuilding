from django.conf.urls import url
from jionparty import views
from django.urls import path

urlpatterns = [
    #"职位列表"

    #设置首页调转到通知页面

    url(r'^apply/$',views.ApplicationCreateView.as_view(),name="apply"),
    url(r'^addprofile/$',views.ProfileCreateView.as_view(),name="addapply"),
    url(r'^change/$',views.ProfileChangeCreateView.as_view(),name="addapply"),
    url(r'^profile/',views.accountProfile,name="profile"),
    path('apply/<int:pk>/',views.applicationDetailView.as_view(),name='apply-detail')
]