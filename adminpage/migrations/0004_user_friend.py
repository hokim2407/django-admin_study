# Generated by Django 3.2.9 on 2022-11-10 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0003_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friend',
            field=models.ManyToManyField(blank=True, related_name='_adminpage_user_friend_+', to='adminpage.User'),
        ),
    ]