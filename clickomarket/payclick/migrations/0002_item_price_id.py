# Generated by Django 5.0.2 on 2024-02-29 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payclick', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price_id',
            field=models.CharField(default='price_0', max_length=50),
            preserve_default=False,
        ),
    ]