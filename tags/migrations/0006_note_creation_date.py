# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-05 18:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0005_note_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='creation_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]