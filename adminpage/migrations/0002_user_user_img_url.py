# Generated by Django 3.2.9 on 2022-11-01 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_img_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='유저 이미지 주소'),
        ),
    ]
