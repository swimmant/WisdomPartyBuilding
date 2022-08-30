import os

from django.contrib import admin, messages

# Register your models here.
from django.forms import model_to_dict
from django.http import HttpResponse

from WisdomPartyBuilding.settings import BASE_DIR
from studyfiles.models import studyFiles


class studyFilesAdmin(admin.ModelAdmin):
    # 在admin页面显示相关属性名称
    # def file_url(self,obj):
    #     if obj.file_http:
    #         return obj.file_http
    #     return ""
    # file_url.allow_tags = True
    # file_url.shrot_description = "文件"
    list_display = ["file_name", "file_type", "file_url", "creator", "create_date", "modified_date"]

    # 隐藏创建人，创建时间，修改人
    # exclude = ("creator", "create_date", "modified_date")

    actions = ['add_file', 'delete_file']

    # 按钮的点击事件
    def add_file(self, modeladmin, request, queryset):
        return True

    # 按钮的配置
    add_file.short_description = '新增文件'
    add_file.type = 'danger'
    add_file.style = 'color:rainbow;'
    add_file.action_type = 0
    add_file.action_url = '/studyfile/'

    # 按钮的点击事件
    def delete_file(self, request, queryset):
        for data in queryset:
            os.remove(os.path.join(BASE_DIR,'static/file/%s' % (data.file_name)))
        messages.add_message(request, messages.INFO, "已删除%s份文件" % (len(queryset)))
        queryset.delete()



# 按钮的配置
    delete_file.short_description = '删除文件'

    list_display_links = None  # 禁用编辑链接

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(self, obj, form, change)


admin.site.register(studyFiles, studyFilesAdmin)
