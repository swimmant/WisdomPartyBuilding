import logging

from django.contrib.auth.models import User
# from  registration.models import
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, Http404
# Create your views here.
# from registration.forms import User

from jionparty.models import Application, Profile

# 快速创建视图
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    # 申请书界面
    template_name = 'application_form.html'
    success_url = "/noticelist/"
    model = Application
    fields = [
        "username", "phone", "age", "email", "born_address", "gender", "identity",
        "college", "major", "degree", "grade", "applicant_introduction",
        "applicant_reason"
    ]

    # 从URL请求参数代入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 将申请书和当前用户关联
    def form_valid(self, form):
        logging.info("保存form")
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileCreateView(LoginRequiredMixin, CreateView):
    # 个人界面
    template_name = 'addProfile.html'
    success_url = "/profile/"
    model = Profile
    fields = [
        "username", "phone", "age", "email", "born_address", "gender", "identity",
        "college", "major", "degree", "grade",
    ]

    # 从URL请求参数代入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 将申请书和当前用户关联
    def form_valid(self, form):
        # logging.info("保存form")
        self.object = form.save(commit=False)
        self.object.auth_user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileChangeCreateView(LoginRequiredMixin, CreateView):
    # 个人界面
    template_name = 'changeProfile.html'
    success_url = "/profile/"
    model = Profile
    fields = [
        "username", "phone", "age", "email", "born_address", "gender", "identity",
        "college", "major", "degree", "grade",
    ]

    # 从URL请求参数代入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 将申请书和当前用户关联
    def form_valid(self, form):
        # logging.info("保存form")
        self.object = form.save(commit=False)
        self.object.auth_user = self.request.user
        account = Profile.objects.filter(auth_user=self.request.user)
        # 找到用户profile，显示user信息
        if account or len(account) > 0:
            account[0].delete()
            self.object.save()

        # 没找到用户profile，添加user信息
        else:
            return HttpResponseRedirect("/addprofile/")

        return HttpResponseRedirect(self.get_success_url())


def accountProfile(request):
    account = Profile.objects.filter(auth_user=request.user)
    applications = Application.objects.filter(applicant=request.user)

    # 找到用户profile，显示user信息
    if account or len(account) > 0:
        return render(request, "profile.html", {"account": account[0], "applicationlist": applications})

    # 没找到用户profile，添加user信息
    else:
        return HttpResponseRedirect("/addprofile/")

    # try:
    #     # 查找相关id的user
    #     notice = Notice.objects.get(pk=notice_id)
    # except notice.DoesNotExist:
    #     raise Http404("通知不存在！")
    #
    # return render(request, 'notice.html', {'notice': notice})


from django.views.generic.detail import DetailView


class applicationDetailView(DetailView):
    model = Application
    template_name = "application_detail.html"
