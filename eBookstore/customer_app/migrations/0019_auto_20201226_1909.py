# Generated by Django 3.1.1 on 2020-12-26 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0018_staff_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='reason',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('error', 'error'), ('process', 'process'), ('finish', 'finish')], default='finish', max_length=12),
        ),
    ]