# Generated by Django 3.2.12 on 2022-04-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220421_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
