# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import helvetic.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorisationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expires', models.DateTimeField(default=helvetic.models._generate_auth_expiry)),
                ('key', models.CharField(default=helvetic.models._generate_auth_key, max_length=10)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField()),
                ('weight', models.PositiveIntegerField(help_text=b'Weight measured, in grams.')),
                ('body_fat', models.DecimalField(help_text=b'Body fat, measured as a percentage.', null=True, max_digits=6, decimal_places=3, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hw_address', models.CharField(help_text=b'Ethernet address of the Aria', max_length=12)),
                ('ssid', models.CharField(max_length=64)),
                ('fw_version', models.PositiveIntegerField(null=True, blank=True)),
                ('battery_percent', models.PositiveIntegerField(null=True, blank=True)),
                ('auth_code', models.BinaryField(max_length=16, null=True, blank=True)),
                ('unit', models.PositiveIntegerField(default=2, help_text=b'Display units for the scale.', choices=[(0, b'Pounds'), (1, b'Stones'), (2, b'Kilograms')])),
                ('owner', models.ForeignKey(help_text=b'Owner of these scales.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(help_text=b'Short name for the user, displayed on the scales', max_length=20)),
                ('birth_date', models.DateField(help_text=b'Date when the user was born.')),
                ('height', models.PositiveIntegerField(help_text=b'Height of the user, in millimetres. Used to calculate body fat.')),
                ('gender', models.PositiveIntegerField(default=52, help_text=b'Biological gender of the user. Used to calculate body fat.', choices=[(2, b'Male'), (0, b'Female'), (52, b'Unknown')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='measurement',
            name='scale',
            field=models.ForeignKey(to='helvetic.Scale'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
