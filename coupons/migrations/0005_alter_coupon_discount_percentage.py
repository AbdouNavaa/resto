# Generated by Django 5.0.6 on 2025-03-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0004_remove_coupon_expires_at_coupon_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_percentage',
            field=models.IntegerField(),
        ),
    ]
