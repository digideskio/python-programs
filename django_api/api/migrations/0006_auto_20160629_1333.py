# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160629_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='CreateComment',
        ),
        migrations.AddField(
            model_name='states',
            name='comment',
            field=models.ManyToManyField(to='api.Comment'),
        ),
    ]