# Generated by Django 5.0.6 on 2025-03-15 16:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0003_alter_coupon_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='expires_at',
        ),
        migrations.AddField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
