# Generated by Django 5.0.2 on 2024-03-01 01:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payclick', '0006_item_currency_order_discount_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='order',
        ),
        migrations.RemoveField(
            model_name='tax',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='payclick.discount'),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='payclick.tax'),
        ),
    ]
