# Generated by Django 2.2.10 on 2021-07-20 14:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_auto_20210720_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='via_money',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='via_points',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 19, 9, 51, 632580)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 19, 9, 51, 635583)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 19, 9, 51, 636583)),
        ),
    ]
