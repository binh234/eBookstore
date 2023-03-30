# eBookstore

A web-based application that allows users to browse, search, and purchase books online. The goal is to provide a convenient and efficient way for users to buy books online while giving the bookstore a digital platform to expand their reach and manage their inventory.

![homepage](screenshots/customer/home1.png)

## Customer

- [x] Secure login/logout
- [x] Search functionalities
- [x] Book details
- [x] Recommended books
- [x] Card checking
- [x] Cart
- [x] Checkout
- [x] View and update profile
- [x] Secure online payment with Momo API
- [x] Fully responsive

## Manager

- [x] Secure login/logout
- [x] Dashboard with statistics
- [x] View and update profile
- [x] Manage books
- [x] Manage orders
- [x] Manage inventory

## Screenshots

<details>
  <summary><b>Customer</b></summary>
  <img src="screenshots/customer/login.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/customer/home1.png" alt="screenshot">
  <img src="screenshots/customer/home2.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/customer/shop.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/customer/book1.png" alt="screenshot">
  <img src="screenshots/customer/book2.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/customer/cart.png" alt="screenshot">
  <img src="screenshots/customer/checkout.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/customer/card.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/customer/order.png" alt="screenshot">
  <img src="screenshots/customer/author.png" alt="screenshot">
</details>

<details>
  <summary><b>Manager</b></summary>
  <img src="screenshots/staff/dashboard.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/staff/author.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/staff/storage.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/staff/book.png" alt="screenshot">
  <img src="screenshots/staff/book2.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/staff/order_detail.png" alt="screenshot">
  <br /><br />
  <img src="screenshots/staff/profile.png" alt="screenshot">
</details>

## Clone project

```bash
git clone https://github.com/binh234/eBookstore.git

cd  eBookstore
```

## Install libraries

```bash
pip install -r requirements.txt
```

## Prepare database

## Setting up database environemnt

Set an environment variable called DATABASE_URL to store your connection string, for example:

- PostgreSQL: `postgresql://username:password@host:port/database_name`
- MySQL: `mysql://username:password@host:port/database_name`

## Migrate data

```bash
# Inside customer directory
python manage.py migrate
```

## Load data

```bash
# Inside customer directory
python manage.py loaddata ../db.json
```

## Customer app development

```bash
cd customer

python manage.py runserver
```

Go to [localhost:8000](http://localhost:8000).

## Staff app development

```bash
cd staff

python manage.py runserver
```

Go to [localhost:8000](http://localhost:8000).
