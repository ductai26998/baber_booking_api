# Generated by Django 3.2.12 on 2022-04-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_baseuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
