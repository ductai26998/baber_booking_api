# Generated by Django 3.2.12 on 2022-04-16 18:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220416_1832'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSalon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.salon')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
    ]
