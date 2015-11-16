# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField()),
                ('source', models.CharField(max_length=10, choices=[(b'M', b'Mandi'), (b'K', b'Kamand')])),
                ('dest', models.CharField(max_length=10, choices=[(b'M', b'Mandi'), (b'K', b'Kamand')])),
                ('seats_left', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('resv', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('bus_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('reg_no', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('vehicle_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('reg_no', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('avail_from', models.DateTimeField(verbose_name=b'Available After')),
                ('avail_till', models.DateTimeField(verbose_name=b'Available Before')),
                ('parked_at', models.CharField(max_length=10, choices=[(b'M', b'Mandi'), (b'K', b'Kamand')])),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('day', models.IntegerField(choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')])),
                ('source', models.CharField(max_length=10, choices=[(b'M', b'Mandi'), (b'K', b'Kamand')])),
                ('dest', models.CharField(max_length=10, choices=[(b'M', b'Mandi'), (b'K', b'Kamand')])),
                ('bus_id', models.ForeignKey(to='main.Bus')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='vehicle_id',
            field=models.ForeignKey(to='main.Car'),
        ),
    ]
