# Generated by Django 5.1.1 on 2024-10-09 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chip_heater', '0008_chip_days_to_heat_chip_heated_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chip',
            name='days_to_heat',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='dias para aquecer'),
        ),
    ]
