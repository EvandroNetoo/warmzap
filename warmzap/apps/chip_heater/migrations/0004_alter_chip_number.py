# Generated by Django 5.1.1 on 2024-09-12 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chip_heater', '0003_chip_directory_token_alter_chip_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chip',
            name='number',
            field=models.CharField(max_length=15, verbose_name='número'),
        ),
    ]
