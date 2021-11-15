# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-11-14 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=200)),
                ('number_of_pages', models.IntegerField()),
                ('publisher', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('release_date', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='employees',
        ),
    ]
