from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
from django.utils.html import format_html

fileType = [(0, u"活动"), (1, u"会议"), (2, u"通告"), (3, u"学习")]


class studyFiles(models.Model):
    file_name = models.CharField(max_length=250, blank=False, verbose_name="文件名称")
    file_type = models.SmallIntegerField(null=True,blank=False, choices=fileType, verbose_name="文件类型")
    file_content = models.FileField(upload_to="file/", blank=False, verbose_name="学习文件")
    creator = models.ForeignKey(User, verbose_name="创建人", null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name="创建日期",default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改日期",default=datetime.now)
    file_http = models.CharField(max_length=200,blank=True,null=True,verbose_name='在线地址')

    class Meta:
        db_table = u'studyFile'
        verbose_name = u'学习文件'
        verbose_name_plural = u'学习文件'

        def __init__(self):
            self.studyFile_name = u'学习文件'

        def __unicode__(self):
            return self.studyFile_name

        def __str__(self):
            return self.studyFile_name

    def file_url(self):
        try:
            file_name = self.file_http.split('/')[-1]
        except:
            file_name = self.file_http
        return format_html('<a href="{}" download="{}">{}</a>'.format(self.file_http,file_name,file_name))

    file_url.allow_tags = True
    file_url.short_description = '在线地址'
