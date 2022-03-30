# Generated by Django 2.2.10 on 2021-08-02 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0030_auto_20210802_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 15, 41, 48, 794491)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 15, 41, 48, 798493)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 15, 41, 48, 798493)),
        ),
    ]