# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-17 00:06
from __future__ import unicode_literals

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0003_increase_link_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='search_document',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='party',
            index=django.contrib.postgres.indexes.GinIndex(fields=[b'search_document'], name='parties_par_search__4220e5_gin'),
        ),
    ]
