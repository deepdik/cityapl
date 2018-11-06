# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 05:40
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('desc', models.TextField(blank=True)),
                ('catImg', models.FileField(default='catImg/None/default.svg', upload_to='catImg/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
		('heightField', models.IntegerField(default=0)),
                ('widthField', models.IntegerField(default=0))
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityImg', models.ImageField(default='cityImg/None/default.png', height_field='heightField', upload_to='cityImg/', width_field='widthField')),
                ('heightField', models.IntegerField(default=0)),
                ('widthField', models.IntegerField(default=0)),
                ('city', models.CharField(choices=[('raebareli', 'Raebareli'), ('lucknow', 'Lucknow')], max_length=120)),
                ('state', models.CharField(choices=[('uttar_pradesh', 'Uttar Pradesh'), ('delhi', 'Delhi')], max_length=120)),
                ('country', models.CharField(default='india', max_length=120)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilterTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('desc', models.TextField(blank=True)),
                ('endDate', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('shopName', models.CharField(max_length=250)),
                ('tagline', models.CharField(blank=True, max_length=500)),
                ('bannerImage', models.ImageField(default='shop/None/default.png', height_field='heightField', upload_to=shop.models.upload_location, width_field='widthField')),
                ('widthField', models.IntegerField(default=0)),
                ('heightField', models.IntegerField(default=0)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('mobileNo', models.CharField(max_length=14)),
                ('alternateMobileNo', models.CharField(blank=True, max_length=15)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='longitude/latitude')),
                ('ownerName', models.CharField(blank=True, max_length=250)),
                ('shopAddress', models.TextField()),
                ('shopPinCode', models.PositiveIntegerField()),
                ('openingTime', models.TimeField()),
                ('closingTime', models.TimeField()),
                ('closingDay', models.CharField(choices=[('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('None', 'none')], max_length=250)),
                ('isActive', models.BooleanField()),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.City')),
                ('filterTags', models.ManyToManyField(blank=True, to='shop.FilterTag')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('gis', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('desc', models.TextField(blank=True)),
                ('subCatImg', models.FileField(default='subcatImg/None/default.svg', upload_to='subCatImg/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
            ],
            options={
                'verbose_name_plural': 'SubCategories',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.NullBooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='shop',
            name='subCategory',
            field=models.ManyToManyField(to='shop.SubCategory'),
        ),
        migrations.AddField(
            model_name='offer',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='filtertag',
            name='subCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.SubCategory'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('city', 'state')]),
        ),
    ]