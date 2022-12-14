# Generated by Django 3.2.9 on 2022-11-09 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0002_user_user_img_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('addr1', models.CharField(max_length=200, verbose_name='주소 1')),
                ('addr2', models.CharField(max_length=200, verbose_name='주소 2')),
                ('postcode', models.CharField(max_length=200, verbose_name='우편번호')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='userAddr', to='adminpage.user')),
            ],
            options={
                'verbose_name_plural': '주소',
                'db_table': 'address',
                'managed': True,
            },
        ),
    ]
