# Generated by Django 5.1.1 on 2024-09-13 09:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chip_heater', '0005_chip_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chip',
            name='directory_token',
        ),
        migrations.AddField(
            model_name='chip',
            name='browser_profile',
            field=models.FileField(default=1, upload_to='', validators=[django.core.validators.FileExtensionValidator(['zip'])], verbose_name='perfil do navegador'),
            preserve_default=False,
        ),
    ]
