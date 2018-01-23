# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 21:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0004_auto_20171026_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='user_dashboard.User'),
        ),
    ]