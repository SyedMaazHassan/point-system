# Generated by Django 2.2.10 on 2021-07-20 16:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0018_auto_20210720_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 21, 36, 1, 737686)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 21, 36, 1, 740689)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 21, 36, 1, 741690)),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cust_receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Customer')),
                ('owner_receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Business_Owner')),
            ],
        ),
    ]
