# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('score', models.FloatField()),
                ('nexttime', models.DateTimeField()),
                ('direction', models.CharField(max_length=2, choices=[('CP', 'Characters to Pīnyīn'), ('PC', 'Pīnyīn to Characters'), ('CE', 'Characters to English'), ('EC', 'English to Characters'), ('EP', 'English to Pīnyīn'), ('PE', 'Pīnyīn to Characters')])),
            ],
        ),
        migrations.CreateModel(
            name='Triple',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('pinyin', models.CharField(max_length=400)),
                ('characters', models.CharField(max_length=400)),
                ('english', models.CharField(max_length=400)),
                ('chapter', models.IntegerField()),
                ('quiz', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='triple',
            field=models.ForeignKey(to='threesidedcards.Triple'),
        ),
        migrations.AddField(
            model_name='score',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
