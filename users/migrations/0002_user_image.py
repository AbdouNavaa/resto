# Generated by Django 5.0.6 on 2025-03-15 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default=1, upload_to='users/'),
            preserve_default=False,
        ),
    ]
