# Generated by Django 3.2.12 on 2022-05-12 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_alter_servicesalon_salon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
