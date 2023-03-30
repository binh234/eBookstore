# Generated by Django 3.0.8 on 2020-11-21 06:57

import creditcards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(blank=True, max_length=254)),
            ],
            options={
                "db_table": "author",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "ISBN",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=80)),
                ("year", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("description", models.TextField(blank=True, max_length=600)),
            ],
            options={
                "db_table": "book",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Book_Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="")),
            ],
            options={
                "db_table": "book_image",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="BookAuthor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "book_author",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ownerName", models.CharField(max_length=50)),
                ("code", creditcards.models.CardNumberField(max_length=20)),
                ("bank", models.CharField(max_length=50)),
                ("branch", models.CharField(blank=True, max_length=50)),
                ("expireDate", models.DateField()),
            ],
            options={
                "db_table": "card",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("name", models.CharField(blank=True, max_length=100)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("address", models.CharField(blank=True, max_length=120)),
                ("avatar", models.ImageField(blank=True, upload_to="")),
            ],
            options={
                "db_table": "customer",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Keyword",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("keyword", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "keyword",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("orderTime", models.DateTimeField(null=True)),
                ("lastUpdate", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Unpaid", "Unpaid"),
                            ("Pending", "Pending"),
                            ("Delivered", "Delivered"),
                            ("Cancel", "Cancel"),
                            ("Error", "Error"),
                        ],
                        default="Unpaid",
                        max_length=20,
                    ),
                ),
                ("shippingAddress", models.CharField(blank=True, max_length=120)),
                ("complete", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "order",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=0)),
                (
                    "option",
                    models.CharField(
                        choices=[
                            ("buy", "mua sách truyền thống"),
                            ("eBuy", "mua sách điện tử"),
                            ("eRent", "thuê sách điện tử"),
                        ],
                        default="buy",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "order_item",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("paymentTime", models.DateTimeField(auto_now_add=True)),
                (
                    "method",
                    models.CharField(
                        choices=[("credit", "credit"), ("transfer", "transfer")],
                        default="transfer",
                        max_length=12,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "db_table": "payment",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=20)),
            ],
            options={
                "db_table": "publisher",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reviewTime", models.DateTimeField(auto_now_add=True)),
                ("comment", models.CharField(max_length=400)),
                (
                    "rating",
                    models.IntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
                    ),
                ),
            ],
            options={
                "db_table": "review",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("name", models.CharField(blank=True, max_length=100)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("avatar", models.ImageField(blank=True, upload_to="")),
            ],
            options={
                "db_table": "staff",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Storage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("country", models.CharField(max_length=20)),
                ("location", models.CharField(max_length=120)),
            ],
            options={
                "db_table": "storage",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "topic",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Electronic",
            fields=[
                (
                    "book",
                    models.OneToOneField(
                        db_column="ISBN",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="customer_app.Book",
                    ),
                ),
                ("rentPrice", models.DecimalField(decimal_places=2, max_digits=10)),
                ("rentDuration", models.IntegerField(default=1)),
                ("link", models.FileField(upload_to="uploads/")),
            ],
            options={
                "db_table": "electronic",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Traditional",
            fields=[
                (
                    "book",
                    models.OneToOneField(
                        db_column="ISBN",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="customer_app.Book",
                    ),
                ),
                ("allowNumber", models.IntegerField(default=1)),
            ],
            options={
                "db_table": "traditional",
                "managed": False,
            },
        ),
    ]
