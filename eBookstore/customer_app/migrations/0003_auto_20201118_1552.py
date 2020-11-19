# Generated by Django 3.0.8 on 2020-11-18 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0002_auto_20201118_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='allow_number',
        ),
        migrations.RemoveField(
            model_name='book',
            name='electronic',
        ),
        migrations.RemoveField(
            model_name='book',
            name='rent_duration',
        ),
        migrations.RemoveField(
            model_name='book',
            name='rent_price',
        ),
        migrations.RemoveField(
            model_name='book',
            name='traditional',
        ),
        migrations.CreateModel(
            name='Traditional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_number', models.IntegerField(default=1)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer_app.Book')),
            ],
            options={
                'db_table': 'traditional',
            },
        ),
        migrations.CreateModel(
            name='Electronic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rent_duration', models.IntegerField(default=1)),
                ('link', models.FileField(upload_to='uploads/')),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer_app.Book')),
            ],
            options={
                'db_table': 'electronic',
            },
        ),
    ]
