# Generated by Django 3.2 on 2022-03-06 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jionparty', '0012_alter_candidate_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=135, verbose_name='姓名')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('phone', models.CharField(max_length=135, verbose_name='手机号码')),
                ('email', models.EmailField(blank=True, max_length=135, verbose_name='邮箱')),
                ('born_address', models.CharField(blank=True, max_length=135, verbose_name='籍贯')),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=135, verbose_name='性别')),
                ('identity', models.CharField(choices=[('群众', '群众'), ('团员', '团员'), ('成年团员', '成年团员'), ('积极分子', '积极分子'), ('预备党员', '预备党员'), ('党员', '党员')], max_length=135, verbose_name='政治面貌')),
                ('college', models.CharField(blank=True, max_length=135, verbose_name='学院')),
                ('major', models.CharField(blank=True, max_length=135, verbose_name='专业')),
                ('degree', models.CharField(blank=True, choices=[('本科', '本科'), ('硕士', '硕士'), ('博士', '博士')], max_length=135, verbose_name='学历')),
                ('grade', models.CharField(blank=True, max_length=135, verbose_name='年级')),
                ('created_date', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('modified_date', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('last_editor', models.CharField(blank=True, max_length=256, verbose_name='最后编辑者')),
                ('applicant_introduction_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jionparty.application', verbose_name='入党申请书')),
                ('applicant_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jionparty.candidate', verbose_name='入党状态')),
                ('auth_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='账号')),
            ],
            options={
                'verbose_name': '个人信息',
                'verbose_name_plural': '个人信息',
            },
        ),
    ]
