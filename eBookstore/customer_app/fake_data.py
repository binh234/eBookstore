from faker import Faker
from customer_app.models import *
import random
from random import randint
from datetime import datetime

faker = Faker()

authors = Author.objects.all()
topics = ['Chính trị', 'Văn học', 'Tiểu thuyết', 'Truyện tranh', 'Thiếu nhi', 'Lịch sử', 'Đời sống', "Kinh tế", 'Nấu ăn', 'Gia đình',
	'Khoa học', 'Vũ trụ', 'Giáo dục', 'Văn hóa', 'Môi trường', 'Sinh học', 'Động vật', 'Thế giới', 'Tình cảm', 'Toán học', 'Trinh thám'
]
publishers = Publisher.objects.all()

for i in range(18000):
	book = Book(
		ISBN = faker.isbn13(separator=''),
		name = faker.sentence(),
		year = int(faker.year()),
		price = randint(20, 200) * 1000.0,
		description = faker.text(300),
		publisher = random.choice(publishers)
	)
	book.save()

	traditional = faker.boolean()
	if traditional:
		allow_number = randint(1,20)
		Traditional.objects.create(book=book, allow_number=allow_number)

	electronic = faker.boolean()
	if electronic or not traditional:
		rent_price = randint(10, 50) * 1000.0
		rent_duration = randint(1, 7)
		Electronic.objects.create(book=book, rent_price=rent_price, rent_duration=rent_duration)

	k = randint(1, 3)
	m = randint(1, 4)
	author_rand = random.choices(authors, k=k)
	topic_rand = set(random.choices(topics, k=m))
	keyword_rand = set([faker.word() for i in range(m)])

	book.authors.add(*author_rand)
	[Topic.objects.create(book=book, name=x) for x in topic_rand]
	[Keyword.objects.create(book=book, keyword=x) for x in keyword_rand]

storages = Storage.objects.all()
traditionals = Traditional.objects.all()
customers = Customer.objects.all()

for i in range(40):
	Staff.objects.create(
		storage = random.choice(storages),
		user=None,
		email = faker.email(),
		firstName = faker.first_name(),
		lastName = faker.last_name(),
		phone = '0' +str(faker.random_int(902387328, 999999999)),
		address = faker.address(),
		avatar=None
	)

for storage in storages:
	n = faker.random_int(50, 60)
	book_rand = set(random.choices(traditionals, k=n))
	staffs = Staff.objects.filter(storage=storage)
	for book in book_rand:
		q = faker.random_int(3, 20)
		Import.objects.create(book=book, 
			storage=storage, importTime=faker.date_time_this_century(), quantity=q, staff=random.choice(staffs))
		Inventory.objects.create(book=book, storage=storage, quantity=q)

for storage in storages:
	n = faker.random_int(5, 20)
	book_rand = set(random.choices(traditionals, k=n))
	staffs = Staff.objects.filter(storage=storage)
	for book in book_rand:
		q = faker.random_int(1, 10)
		Export.objects.create(book=book, 
			storage=storage, exportTime=faker.date_time_this_century(), quantity=q, staff=random.choice(staffs))

books = Book.objects.all()
for book in books:
	n = faker.random_int(0, 7)
	customer_rand = set(random.choices(customers, k=n))
	for customer in customer_rand:
		Review.objects.create(customer=customer, 
			book=book, 
			reviewTime=faker.date_time_this_century(),
			comment=faker.text(250),
			rating=randint(1, 5))

statuses = ['Unpaid', 'Pending', 'Delivered', 'Cancel', 'Error']
customer_rand = random.choices(customers, k=10)
for customer in customer_rand:
	Order.objects.create(customer=customer,
		orderTime=faker.date_time_this_year(),
		status = random.choice(statuses),
		shippingAddress=faker.address(),
		complete=True)

option = ['buy', 'eBuy', 'eRent']
orders = Order.objects.filter(id__gt=3)
for order in orders:
	q = faker.random_int(1, 3)
	book_rand = set(random.choices(books, k=q))
	for book in book_rand:
		n = faker.random_int(1, 5)
		OrderItem.objects.create(book=book, order=order, quantity=n, option='buy')


exports = Export.objects.all()
imports = Import.objects.all()
reviews = Review.objects.all()

for item in imports:
	item.importTime = faker.date_time_this_month()
	item.save()

for item in exports:
	item.exportTime = faker.date_time_this_month()
	item.save()

for item in reviews:
	item.reviewTime = faker.date_time_this_century()
	item.save()

exports = Export.objects.all()
imports = Import.objects.all()
for item in imports:
	staffs = Staff.objects.filter(storage=item.storage)
	item.staff = random.choice(staffs)
	item.save()

for item in exports:
	staffs = Staff.objects.filter(storage=item.storage)
	item.staff = random.choice(staffs)
	item.save()

statuses = ['Pending']
customers = Customer.objects.all()
staffs = Staff.objects.all()
for _ in range(50):
	customer = random.choice(customers)
	status = random.choice(statuses)
	if status != 'Unpaid':
		staff = random.choice(staffs)
	else:
		staff = None
	Order.objects.create(customer=customer,
		staff=staff,
		orderTime=faker.date_time_this_month(after_now=True),
		status = status,
		shippingAddress=faker.address(),
		complete=True)

orders = Order.objects.filter(status='Pending').filter(staff__isnull=True)
for order in orders:
	staff = random.choice(staffs)
	order.staff = staff
	order.save()

options = ['buy', 'eBuy', 'eRent']
orders = Order.objects.filter(id__gt=115)
traditionals = Traditional.objects.all()
electronics = Electronic.objects.all()
books = Book.objects.all()
for order in orders:
	q = randint(2, 10)
	book_rand = set(random.choices(books, k=q))
	for book in book_rand:
		n = randint(1, 5)
		try:
			elec = book.electronic
			option = random.choice(options)
			if option == 'eBuy':
				n = 1
		except:
			option = 'buy'
		
		OrderItem.objects.create(book=book, order=order, quantity=n, option=option)

traditionals = Traditional.objects.all()
storages = Storage.objects.all()
for storage in storages:
	n = faker.random_int(40, 50)
	book_rand = set(random.choices(traditionals, k=n))
	staffs = Staff.objects.filter(storage=storage)
	for book in book_rand:
		q = faker.random_int(3, 20)
		Import.objects.create(book=book, 
			storage=storage, importTime=faker.date_time_this_month(), quantity=q, staff=random.choice(staffs))
		item_list = Inventory.objects.filter(book=book, storage=storage)
		if item_list:
			item = item_list[0]
			item.quantity += q
			item.save()
		else:
			Inventory.objects.create(book=book, storage=storage, quantity=q)

for storage in storages:
	n = faker.random_int(5, 20)
	book_rand = set(random.choices(traditionals, k=n))
	staffs = Staff.objects.filter(storage=storage)
	for book in book_rand:
		q = faker.random_int(1, 10)
		Export.objects.create(book=book, 
			storage=storage, exportTime=faker.date_time_this_month(), quantity=q, staff=random.choice(staffs))

payment_statuses = ['finish']
orders = Order.objects.filter(id__gt=115).exclude(status='Unpaid').prefetch_related('orderitem_set')

order = Order.objects.filter(orderTime__gte='2020-12-30')
for order in orders:
	status = random.choice(payment_statuses)
	if status != 'finish':
		reason = faker.text(100)
	else:
		reason = ""
	Payment.objects.create(
		customer=order.customer,
		order=order,
		method='credit',
		amount=order.total,
		status=status,
		reason=reason
	)

payments = Payment.objects.filter(id__gt=2)
for payment in payments:
	status = payment.status[2:-2]
	payment.status = status
	payment.paymentTime = payment.order.orderTime
	payment.save()

orders = Order.objects.filter(orderTime__gte='2020-12-30')
for order in orders:
	order.orderTime = faker.date_time_this_month()
	order.save()

payments = Payment.objects.filter(paymentTime__gte='2020-12-30')
for payment in payments:
	payment.paymentTime = payment.order.orderTime	