# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-29 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0018_question_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bold', models.TextField()),
                ('content', models.TextField()),
                ('img', models.TextField()),
                ('img1', models.TextField()),
                ('number_of_theme', models.IntegerField()),
                ('number_of_question', models.IntegerField()),
            ],
        ),
    ]