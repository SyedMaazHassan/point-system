# Generated by Django 2.2.10 on 2021-07-23 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0022_auto_20210720_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='current_membership_level',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 23, 19, 32, 32, 857426)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 23, 19, 32, 32, 860428)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 23, 19, 32, 32, 861428)),
        ),
    ]