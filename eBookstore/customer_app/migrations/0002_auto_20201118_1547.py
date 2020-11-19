# Generated by Django 3.0.8 on 2020-11-18 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='staff',
            field=models.ForeignKey(blank=True, db_column='staffId', null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer_app.Staff'),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='card',
            name='branch',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='shippingAddress',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(db_column='orderId', on_delete=django.db.models.deletion.CASCADE, to='customer_app.Order'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='staff',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='staff',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='staff',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='book_image',
            unique_together={('book', 'image')},
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together={('customer', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='export',
            unique_together={('book', 'storage')},
        ),
        migrations.AlterUniqueTogether(
            name='import',
            unique_together={('book', 'storage')},
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('book', 'storage')},
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together={('book', 'keyword')},
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('book', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('customer', 'book')},
        ),
    ]
