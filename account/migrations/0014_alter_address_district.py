# Generated by Django 3.2.12 on 2022-04-24 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20220424_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, help_text='Quận/huyện/thành phố không trực thuộc', max_length=128, null=True),
        ),
    ]
