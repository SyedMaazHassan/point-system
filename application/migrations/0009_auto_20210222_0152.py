# Generated by Django 3.1.2 on 2021-02-22 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_business_owner_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 1, 52, 14, 993938)),
        ),
        migrations.AddField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 1, 52, 14, 993938)),
        ),
    ]
