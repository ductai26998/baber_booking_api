# Generated by Django 3.2.12 on 2022-04-24 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_address_district'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseuser',
            options={'ordering': ('date_joined',)},
        ),
    ]
