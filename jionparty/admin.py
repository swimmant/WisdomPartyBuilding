import logging

from django.contrib import admin
from jionparty.models import Candidate, Profile
from django.http.response import HttpResponse
from datetime import datetime
from django.db.models import Q
import csv
from jionparty.models import Application
from django.contrib import messages

from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

exportable_fields = ("username", "user_age", "user_city", "user_phone", "user_email", "user_address",
                     "user_gender", "user_remark", "user_major", "user_degree", "user_identity",
                     "branch_name", "branch_manager_user", "branch_comment",
                     )


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response["Content-Disposition"] = 'attachment;filename=jionparty-candidate' \
                                      '-list-%s.csv' % (
                                          datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                                      )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    for obj in queryset:
        # 单行记录写入csv
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.info("%s 导出 %s 候选人信息" % (request.user, len(queryset)))
    return response

    # 设置导出功能别名


export_model_as_csv.short_description = u'导出csv文件'
export_model_as_csv.allowed_permissions = ("export",)





class CandidateAdmin(admin.ModelAdmin):
    # 添加功能
    actions = [export_model_as_csv, ]

    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    exclude = ["userid", "creator", "created_date", "modified_date", "last_editor"]

    # def get_exclude(self, request, obj=None):
    #     group_name = self.get_group_names(request.user)
    #     if 'branchManager' in group_name:
    #         logger.info("manage is in user's group for %s" % request.user.username)
    #         return ("userid", "creator", "created_date", "modified_date", "last_editor",
    #                 "branch_manager_user", "master_manager_user", "audit_result",
    #                 "audit_comment",)
    #     return ()
    list_display = ["username","get_application","user_age", "user_city", "user_phone", "user_email", "user_address",
                    "user_gender", "user_college", "user_major", "user_degree", "user_identity",
                    "branch_name", "branch_manager_user", "branch_comment", "audit_result", "user_remark", ]

    # 筛选条件
    list_filter = ("user_identity", "user_major", "user_degree", "branch_name", "user_college")

    # 查寻
    search_fields = ("username", "user_phone", "branch_name", "user_college")
    ordering = ("user_identity", "user_degree", "user_major", "user_college")

    # readonly_fields = ("branch_manager_user", "master_manager_user", "audit_result", "audit_comment",)
    default_list_editable = (
        "user_identity", "user_major", "user_college", "branch_name", "branch_manager_user", "audit_result",)

    def get_application(self, obj):
        if not obj.user_phone:
            return ""
        application = Application.objects.filter(phone=obj.user_phone)
        if application and len(application) > 0:
            return mark_safe(
                u'<a href="/apply/%s" target="_blank">%s</a>' % (application[0].id,"查看申请")
            )
    get_application.short_description = "查看申请"
    get_application.allow_tags = True

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        # logger.info("user is request.user.is_super_user ?", request.user.is_superuser)
        if request.user.is_superuser or 'auditManager' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    # 设置只读字段
    def get_readonly_fields(self, request, obj=None):
        group_name = self.get_group_names(request.user)
        print("------------------")
        if 'branchManager' in group_name:
            logger.info("manage is in user's group for %s" % request.user.username)
            return ("user_identity", "branch_name", "branch_manager_user", "master_manager_user", "audit_result",
                    "audit_comment",)
        return ()

    fieldsets = (
        ("基础信息", {'fields': (("username", "user_age", "user_gender"),
                             ("user_college", "user_major",), ("user_degree", "user_identity")), }),
        ("个人信息", {'fields': (("user_phone", "user_email",), ("user_city", "user_address",))}),
        ("支部信息", {'fields': ("branch_name", "branch_manager_user", ("branch_comment",))}),
        ("总管理员", {'fields': ("master_manager_user", "audit_result", ("audit_comment",))})
    )

    # default_branch_fieldsets = (
    #     ("基础信息", {'fields': (("username", "user_age", "user_gender"),
    #                          ("user_college", "user_major",), ("user_degree", "user_identity")), }),
    #     ("个人信息", {'fields': (("user_phone", "user_email",), ("user_city", "user_address",))}),
    #     ("支部信息", {'fields': ("branch_name", "branch_manager_user", ("branch_comment",))}),
    # )
    #

    # 设置支部和管理员意见是否可见
    # def get_fieldsets(self, request, obj=None):
    # pass

    # 对数据集权限进行管理
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'auditManager' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(branch_manager_user=request.user)
        )


# 定义审核申请操作
def application_process(modeadmin, request, queryset):
    candidate_names = ""
    for apply in queryset:
        candidate = Candidate()
        # 将申请书对象拷贝给candidate对象中
        # candidate.__dict__.update(apply.__dict__)
        candidate.username = apply.username
        candidate.user_city = apply.born_address
        candidate.user_age = apply.age
        candidate.user_email = apply.email
        candidate.user_phone = apply.phone
        candidate.user_gender = apply.gender
        candidate.user_identity = apply.identity
        candidate.user_college = apply.college
        candidate.user_major = apply.major
        candidate.user_degree = apply.degree
        candidate.user_grade = apply.grade
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + "," + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, "候选人：%s成功进入审批流程" % (candidate_names))


application_process.short_description = u'进入审批流程'
application_process.allowed_permissions = ("process",)


class ApplicationAdmin(admin.ModelAdmin):
    actions = (application_process,)

    def has_process_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "process"))

    list_display = ("username", "applicant", "age","gender", "grade", "college", "major", "identity", "created_date")
    readonly_fields = ("applicant", "created_date", "modified_date",)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username","age", "gender", "identity"),
            ("email", "phone", "born_address"),
            ("college", "major", "grade"),
            "applicant_introduction", "applicant_reason",
        )}),

    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):

    list_display = ("username", "auth_user", "age","gender", "grade", "college", "major", "identity", "created_date")
    readonly_fields = ("auth_user", "created_date", "modified_date",)

    fieldsets = (
        (None, {'fields': (
            "auth_user", ("username", "age", "gender", "identity"),
            ("email", "phone", "born_address"),
            ("college", "major", "grade"),
            "applicant_introduction_record", "applicant_status",
        )}),

    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Profile, ProfileAdmin)
