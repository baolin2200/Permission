# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-10 04:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='group_menu',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='组内菜单'),
        ),
        migrations.AddField(
            model_name='permissiongroup',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单'),
        ),
    ]
