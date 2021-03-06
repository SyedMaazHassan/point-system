# Generated by Django 2.2.10 on 2021-08-02 10:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0028_auto_20210727_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='status',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 15, 26, 43, 741557)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 15, 26, 43, 745541)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 15, 26, 43, 746542)),
        ),
    ]
