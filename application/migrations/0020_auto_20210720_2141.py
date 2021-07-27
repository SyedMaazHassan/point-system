# Generated by Django 2.2.10 on 2021-07-20 16:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0019_auto_20210720_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 21, 41, 33, 797582)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 21, 41, 33, 800584)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 21, 41, 33, 801585)),
        ),
    ]
