# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-23 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0017_remove_question_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
