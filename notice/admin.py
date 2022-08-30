from django.contrib import admin

# Register your models here.
from notice.models import Notice


class NoticeAdmin(admin.ModelAdmin):
    # 在admin页面显示相关属性名称
    list_display = ["notice_name", "notice_type", "creator", "create_date", "modified_date"]

    # 隐藏创建人，创建时间，修改人
    exclude = ("creator", "create_date", "modified_date")

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(self, obj, form, change)


admin.site.register(Notice, NoticeAdmin)
