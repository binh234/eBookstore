from faker import Faker
from customer_app.models import *
import random
from random import randint

faker = Faker()

authors = Author.objects.all()
topics = ['Chính trị', 'Văn học', 'Tiểu thuyết', 'Truyện tranh', 'Thiếu nhi', 'Lịch sử', 'Đời sống', "Kinh tế", 'Nấu ăn', 'Gia đình',
	'Khoa học', 'Vũ trụ', 'Giáo dục', 'Văn hóa', 'Môi trường', 'Sinh học', 'Động vật', 'Thế giới', 'Tình cảm', 'Toán học', 'Trinh thám'
]
publishers = Publisher.objects.all()

for i in range(50):
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

for storage in storages:
	n = faker.random_int(50, 60)
	book_rand = set(random.choices(traditionals, k=n))
	for book in book_rand:
		q = faker.random_int(3, 20)
		Import.objects.create(book=book, storage=storage, importTime=faker.date_time_this_century(), quantity=q)
		Inventory.objects.create(book=book, storage=storage, quantity=q)

for storage in storages:
	n = faker.random_int(5, 20)
	book_rand = set(random.choices(traditionals, k=n))
	for book in book_rand:
		q = faker.random_int(1, 10)
		Export.objects.create(book=book, storage=storage, exportTime=faker.date_time_this_century(), quantity=q)

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


