# Generated by Django 3.2.12 on 2022-04-03 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220403_0314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salon',
            options={'ordering': ('date_joined',)},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('date_joined',)},
        ),
    ]
