# Generated by Django 5.0.6 on 2025-03-15 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='status',
            field=models.CharField(choices=[('مفعل', 'مفعل'), ('معطل', 'معطل')], default='قيد التنفيذ', max_length=20),
        ),
        migrations.AddField(
            model_name='coupon',
            name='use_number',
            field=models.IntegerField(default=0),
        ),
    ]
