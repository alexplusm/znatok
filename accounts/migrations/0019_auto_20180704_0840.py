# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-04 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_rank_rank_img_disable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank_progress',
            field=models.IntegerField(default=100),
        ),
    ]