# Generated by Django 3.1.1 on 2020-12-25 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0017_auto_20201122_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='address',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]