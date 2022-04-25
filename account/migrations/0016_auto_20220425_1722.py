# Generated by Django 3.2.12 on 2022-04-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_baseuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='position_url',
            field=models.CharField(blank=True, help_text='Url của vị trí trên google map', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(blank=True, help_text='Địa chỉ cụ thể', max_length=512, null=True),
        ),
    ]
