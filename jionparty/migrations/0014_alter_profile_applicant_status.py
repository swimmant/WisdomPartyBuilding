# Generated by Django 3.2 on 2022-03-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jionparty', '0013_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='applicant_status',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='入党状态'),
        ),
    ]