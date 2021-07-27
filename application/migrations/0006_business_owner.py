# Generated by Django 3.1.2 on 2021-02-21 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0005_delete_place_information'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business_Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_first_name', models.CharField(max_length=50)),
                ('owner_last_name', models.CharField(max_length=50)),
                ('business_email', models.CharField(max_length=50)),
                ('business_telephone', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
