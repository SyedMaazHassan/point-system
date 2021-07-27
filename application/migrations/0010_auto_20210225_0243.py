# Generated by Django 3.1.2 on 2021-02-25 10:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_auto_20210222_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_owner',
            name='organization_no',
            field=models.CharField(default='None', max_length=11),
        ),
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 25, 2, 43, 8, 158188)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 25, 2, 43, 8, 158188)),
        ),
    ]
