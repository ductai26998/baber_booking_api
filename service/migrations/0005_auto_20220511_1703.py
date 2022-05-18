# Generated by Django 3.2.12 on 2022-05-11 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20220511_1649'),
        ('service', '0004_remove_service_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesalon',
            name='salon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='account.salon'),
        ),
        migrations.AlterField(
            model_name='servicesalon',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_salon', to='service.service'),
        ),
    ]
