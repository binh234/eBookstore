# Generated by Django 3.0.8 on 2020-11-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0013_auto_20201121_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='firstName',
            field=models.CharField(default='Borg', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='lastName',
            field=models.CharField(default='Inc', max_length=30),
        ),
        migrations.AddField(
            model_name='staff',
            name='firstName',
            field=models.CharField(default='Borg', max_length=50),
        ),
        migrations.AddField(
            model_name='staff',
            name='lastName',
            field=models.CharField(default='Inc', max_length=30),
        ),
    ]
