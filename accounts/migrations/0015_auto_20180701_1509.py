# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-01 15:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_profile_rank'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ranks',
            new_name='Rank',
        ),
    ]