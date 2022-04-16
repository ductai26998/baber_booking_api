# Generated by Django 3.2.12 on 2022-04-16 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_servicesalon'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesalon',
            name='currency',
            field=models.CharField(default='VND', max_length=3),
        ),
        migrations.AddField(
            model_name='servicesalon',
            name='price_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
    ]