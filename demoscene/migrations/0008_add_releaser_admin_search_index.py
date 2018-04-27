# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-22 01:31
from __future__ import unicode_literals

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoscene', '0007_nickvariant_search_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='releaser',
            name='admin_search_document',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='releaser',
            index=django.contrib.postgres.indexes.GinIndex(fields=[b'admin_search_document'], name='demoscene_r_admin_s_a0c2dc_gin'),
        ),
    ]