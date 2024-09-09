# Generated by Django 5.1.1 on 2024-09-08 20:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chip_heater', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chip',
            name='number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Número de telefone inválido. O formato deve ser (xx) xxxx-xxxx ou (xx) xxxxx-xxxx.', regex='^\\(\\d{2}\\) \\d{4}-\\d{4}$|^\\(\\d{2}\\) \\d{5}-\\d{4}$')], verbose_name='número'),
        ),
    ]
