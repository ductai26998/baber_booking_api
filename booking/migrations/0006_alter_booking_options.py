# Generated by Django 3.2.12 on 2022-06-14 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20220613_1929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('-created_at',)},
        ),
    ]
