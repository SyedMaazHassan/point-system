# Generated by Django 3.1.2 on 2021-02-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_owner',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
