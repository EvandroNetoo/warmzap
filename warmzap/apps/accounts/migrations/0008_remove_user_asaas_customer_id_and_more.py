# Generated by Django 5.1.1 on 2024-10-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_asaas_customer_id_user_asaas_subscription_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='asaas_customer_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='asaas_subscription_id',
        ),
        migrations.AddField(
            model_name='user',
            name='asaas_customer',
            field=models.JSONField(blank=True, null=True, verbose_name='clinte do asaas'),
        ),
        migrations.AddField(
            model_name='user',
            name='asaas_subscription',
            field=models.JSONField(blank=True, null=True, verbose_name='assinatura do asaas'),
        ),
    ]
