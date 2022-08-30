from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
NoticeType = [(0, "活动"), (1, "会议"), (2, "通告"), (3, "新闻")]


class Notice(models.Model):
    notice_type = models.SmallIntegerField(blank=False, choices=NoticeType, verbose_name="通知类别")
    notice_name = models.CharField(max_length=250, blank=False, verbose_name="通知名称")
    notice_content = models.TextField(max_length=1024, blank=False, verbose_name="通知内容")
    creator = models.ForeignKey(User, verbose_name="创建人", null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name="创建日期",default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改日期",default=datetime.now)

    class Meta:
        db_table = u'notice'
        verbose_name = u'通知'
        verbose_name_plural = u'通知'

        def __init__(self):
            self.notice_name = u'通知'

        def __unicode__(self):
            return self.notice_name

        def __str__(self):
            return self.notice_name
