# Generated by Django 3.1.2 on 2020-10-18 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0008_auto_20201018_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date',
        ),
    ]