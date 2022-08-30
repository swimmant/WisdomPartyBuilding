# Generated by Django 3.2 on 2022-03-01 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jionparty', '0004_auto_20220228_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='master_manager_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_manager_user', to=settings.AUTH_USER_MODEL, verbose_name='总管理员'),
        ),
    ]
