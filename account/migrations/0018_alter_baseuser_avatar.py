# Generated by Django 3.2.12 on 2022-06-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20220511_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
    ]