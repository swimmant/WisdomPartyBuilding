from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 审批结果
# 入党流程状态
AUDIT_RESULT = ((u'通过', u'通过'), (u'待审核', u'待审核'), (u'否决', u'否决'))

# 账号类型
Count_Type = ((u'非党员', u'非党员'), (u'党员', u'党员'), (u'支部管理员', u'支部管理员'), (u'总管理员', u'总管理员'))

# 性别
Gender_Type = ((u'男', u'男'), (u'女', u'女'))
# 学历
# 学历
Degree_Type = ((u'本科', u'本科'), (u'硕士', u'硕士'), (u'博士', u'博士'))
# 身份
Identity_Type = ((u'群众', u'群众'), (u'团员', u'团员'), (u'成年团员', u'成年团员'), (u'积极分子', '积极分子'),
                 (u'预备党员', u'预备党员'), (u'党员', u'党员'))


class Candidate(models.Model):
    # 基础信息
    userid = models.IntegerField(unique=True, blank=True, null=True, verbose_name=u'候选人ID')
    username = models.CharField(max_length=135, verbose_name=u'姓名')
    user_age = models.IntegerField(blank=True, null=True, verbose_name=u'年龄')
    user_city = models.CharField(max_length=135, verbose_name=u"城市")
    user_phone = models.CharField(max_length=135, verbose_name=u"手机号码")
    user_email = models.CharField(max_length=135, blank=True, verbose_name=u"邮箱")
    user_address = models.CharField(max_length=135, blank=True, verbose_name=u"籍贯")
    user_gender = models.CharField(max_length=135, choices=Gender_Type, null=False, verbose_name=u"性别")
    user_remark = models.CharField(max_length=135, blank=True, verbose_name=u"备注")
    # 学院与专业，年级信息
    user_college = models.CharField(max_length=135, blank=True, verbose_name=u"学院")
    user_major = models.CharField(max_length=135, blank=True, verbose_name=u"专业")
    user_degree = models.CharField(max_length=135, choices=Degree_Type, blank=True, verbose_name=u"学历")
    user_grade = models.CharField(max_length=135, blank=True, verbose_name="年级")

    user_identity = models.CharField(max_length=135, choices=Identity_Type, null=False, verbose_name=u'政治面貌')

    # 支部管理员
    branch_name = models.CharField(max_length=256, blank=True, verbose_name=u'支部名称')
    branch_manager_user = models.ForeignKey(User, related_name="branch_manager_user", blank=True,
                                            null=True, on_delete=models.CASCADE, verbose_name="支部管理员")
    branch_comment = models.TextField(max_length=1024, blank=True, verbose_name=u"支部意见", help_text="该位同志各方面表现情况")
    # 审核信息
    # 审核人
    master_manager_user = models.ForeignKey(User, related_name="master_manager_user", blank=True,
                                            null=True, on_delete=models.CASCADE, verbose_name="总管理员")
    audit_result = models.CharField(max_length=135, blank=False, choices=AUDIT_RESULT, verbose_name="审核结果")
    audit_comment = models.TextField(max_length=1024, blank=True, verbose_name=u"审核意见")
    audit_date = models.DateTimeField(auto_now=True, verbose_name=u'审核时间')
    audit_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="审核更新时间")
    audit_last_editor = models.CharField(max_length=256, blank=True, verbose_name="最后审核者")

    #
    # 创建信息
    creator = models.CharField(max_length=256, blank=True, verbose_name=u'候选人数据创建者')
    created_date = models.DateTimeField(auto_now=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
    last_editor = models.CharField(max_length=256, blank=True, verbose_name="最后编辑者")

    class Meta:
        db_table = u'candidate'
        verbose_name = u'候选人'
        verbose_name_plural = u'候选人'

        permissions = [
            ('export', "能导出候选人数据"),
            ('process', "提交审批"),
        ]

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username


class Application(models.Model):
    # 个人信息
    username = models.CharField(max_length=135, verbose_name=u'姓名')
    applicant = models.ForeignKey(User, verbose_name=u"申请人", null=True, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True, verbose_name=u'年龄')
    phone = models.CharField(max_length=135, verbose_name=u"手机号码")
    email = models.EmailField(max_length=135, blank=True, verbose_name=u"邮箱")
    born_address = models.CharField(max_length=135, blank=True, verbose_name=u"籍贯")
    gender = models.CharField(max_length=135, choices=Gender_Type, verbose_name=u"性别")
    identity = models.CharField(max_length=135, choices=Identity_Type, null=False, verbose_name=u'政治面貌')

    # 年级信息
    college = models.CharField(max_length=135, blank=True, verbose_name=u"学院")
    major = models.CharField(max_length=135, blank=True, verbose_name=u'专业')
    degree = models.CharField(max_length=135, choices=Degree_Type, blank=True, verbose_name=u"学历")
    grade = models.CharField(max_length=135, blank=True, verbose_name="年级")

    # 创建信息
    created_date = models.DateTimeField(auto_now=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
    last_editor = models.CharField(max_length=256, blank=True, verbose_name="最后编辑者")

    # 申请入党信息
    applicant_introduction = models.TextField(max_length=1024, blank=True, verbose_name=u'自我评价')
    applicant_reason = models.TextField(max_length=1024, blank=True, verbose_name=u'入党原由')

    class Meta:
        verbose_name = u'申请'
        verbose_name_plural = u'申请列表'

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username


class Profile(models.Model):
    # 个人信息
    username = models.CharField(max_length=135, verbose_name=u'姓名')
    auth_user = models.ForeignKey(User, verbose_name=u"账号", null=True, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True, verbose_name=u'年龄')
    phone = models.CharField(max_length=135, verbose_name=u"手机号码")
    email = models.EmailField(max_length=135, blank=True, verbose_name=u"邮箱")
    born_address = models.CharField(max_length=135, blank=True, verbose_name=u"籍贯")
    gender = models.CharField(max_length=135, choices=Gender_Type, verbose_name=u"性别")
    identity = models.CharField(max_length=135, choices=Identity_Type, null=False, verbose_name=u'政治面貌')

    # 年级信息
    college = models.CharField(max_length=135, blank=True, verbose_name=u"学院")
    major = models.CharField(max_length=135, blank=True, verbose_name=u'专业')
    degree = models.CharField(max_length=135, choices=Degree_Type, blank=True, verbose_name=u"学历")
    grade = models.CharField(max_length=135, blank=True, verbose_name="年级")

    # 创建信息
    created_date = models.DateTimeField(auto_now=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
    last_editor = models.CharField(max_length=256, blank=True, verbose_name="最后编辑者")

    # 入党信息
    applicant_introduction_record = models.ForeignKey(Application,null=True,verbose_name="入党申请书",on_delete=models.SET_NULL)
    applicant_status = models.CharField(max_length=256, null=True,blank=True, verbose_name="入党状态")

    class Meta:
        verbose_name = u'个人信息'
        verbose_name_plural = u'个人信息'
