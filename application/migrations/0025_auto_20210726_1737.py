# Generated by Django 2.2.10 on 2021-07-26 12:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0024_auto_20210725_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_owner',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 17, 37, 52, 398040)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 17, 37, 52, 401042)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 17, 37, 52, 402042)),
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_to_give', models.FloatField()),
                ('individual_percent', models.FloatField()),
                ('is_completed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Business')),
                ('transfers', models.ManyToManyField(to='application.Transfer')),
            ],
        ),
    ]
