# Generated by Django 3.2.12 on 2022-05-11 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_service_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='gender',
        ),
    ]
