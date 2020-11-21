from django.db import models
from django.contrib.auth.models import User
from creditcards.models import CardNumberField

# Create your models here.	

class Storage(models.Model):
	country = models.CharField(max_length=20)
	location = models.CharField(max_length=120)

	class Meta:
		managed = False
		db_table = 'storage'

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, db_column='userId')
	email = models.EmailField(blank=True)
	name = models.CharField(max_length=100, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=120, blank=True)
	avatar = models.ImageField(blank=True)

	class Meta:
		managed = False
		db_table = 'customer'

	def profile_url(self):
		if self.avatar:
			return self.avatar.url
		return "/static/images/default_profile.jpg"

	def __str__(self):
		return self.name

class Staff(models.Model):
	storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True, db_column='storageId')
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, db_column='userId')
	email = models.EmailField(blank=True)
	name = models.CharField(max_length=100, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	avatar = models.ImageField(blank=True)

	class Meta:
		managed = False
		db_table = 'staff'

	def profile_url(self):
		if self.profile_image:
			return self.profile_image.url
		return "/static/images/default_profile.jpg"

	def __str__(self):
		return self.name

class Order(models.Model):
	ORDER_STATUS = [
		('Unpaid', 'Unpaid'),
		('Pending', 'Pending'),
		('Delivered', 'Delivered'),
		('Cancel', 'Cancel'),
		('Error', 'Error')
	]

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, db_column='customerId')
	staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, db_column='staffId')
	orderTime = models.DateTimeField(null=True)
	lastUpdate = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Unpaid')
	shippingAddress = models.CharField(max_length=120, blank=True)
	complete = models.BooleanField(default=False)

	class Meta:
		managed = False
		db_table = 'order'

	@property
	def shipping(self):
		traditional_item = self.orderitem_set.filter(option='buy')
		return traditional_item.exists()

	def __str__(self):
		return str(self.id) + " - " + str(self.customer)

	def add_item(self, bookISBN, quantity, option, action):
		book = Book.objects.get(ISBN=bookISBN)
		order_item, created = self.orderitem_set.get_or_create(book=book)
		if created == False and order_item.option != option:
			return created, f'Bạn không được phép có 2 lựa chọn mua hàng khác nhau cho cùng một sách'
		order_item.option = option

		if action == 'update':
			order_item.quantity = quantity
		else:
			order_item.quantity += quantity

		if option == "buy" and order_item.quantity > book.allow_number:
			if created:
				order_item.delete()
			return created, f'Số lượng sách {book.name} tối đa được phép mua là: {book.allow_number}'
		elif option == "eBuy" and order_item.quantity > 1:
			return created, f'Số lượng sách điện tử {book.name} được phép mua là: 1'
		else:	
			order_item.save()
		return created, 'success'

	def remove_item(self, bookISBN, option):
		order_item = self.orderitem_set.get(book__ISBN=bookISBN, option=option)
		if order_item:
			order_item.delete()
			return True, "success"
		return False, "Vật phẩm không có trong giỏ hàng"

class Author(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(blank=True)

	class Meta:
		managed = False
		db_table = 'author'

	def __str__(self):
		return self.name	

class Publisher(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField( blank=True)
	phone = models.CharField(max_length=20, blank=True)

	class Meta:
		managed = False
		db_table = 'publisher'

	def __str__(self):
		return self.name

class Book(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=80)
	year = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(max_length=600, blank=True)

	authors = models.ManyToManyField(
        Author,
        through='BookAuthor',
    )
	publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, db_column='publisherId')

	class Meta:
		managed = False
		db_table = 'book'

	def __str__(self):
		return self.name

	@property
	def allow_number(self):
		try:
			return self.traditional.allowNumber
		except:
			return 0

	@property
	def rent_price(self):
		try:
			return self.electronic.rentPrice
		except:
			return 0

	@property
	def rent_duration(self):
		try:
			return self.electronic.rentDuration
		except:
			return 0

	@property
	def image_url(self):
		image = self.book_image_set.first()

		if image is None:
			return ""
		return image.image_url

	@property
	def author_list(self):
		author_name_list = self.authors.values_list('name', flat=True)
		return ", ".join(author_name_list)

	@property
	def topic_list(self):
		topic_name_list = self.topic_set.values_list('name', flat=True)
		return ", ".join(topic_name_list)

	@property
	def keyword_list(self):
		keyword_list = self.keyword_set.values_list('keyword', flat=True)
		return ", ".join(keyword_list)

class Traditional(models.Model):
	book = models.OneToOneField(Book, on_delete=models.CASCADE, db_column='ISBN', primary_key=True)
	allowNumber = models.IntegerField(default=1)

	class Meta:
		managed = False
		db_table = 'traditional'

class Electronic(models.Model):
	book = models.OneToOneField(Book, on_delete=models.CASCADE, db_column='ISBN', primary_key=True)
	rentPrice = models.DecimalField(max_digits=10, decimal_places=2)
	rentDuration = models.IntegerField(default=1)
	link = models.FileField(upload_to='uploads/')

	class Meta:
		managed = False
		db_table = 'electronic'

class BookAuthor(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookISBN')
	author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='authorId')

	class Meta:
		managed = False
		db_table = 'book_author'
		unique_together = (('book', 'author'))
			

class OrderItem(models.Model):
	OPTION = [
		('buy', 'mua sách truyền thống'),
		('eBuy', 'mua sách điện tử'),
		('eRent', 'thuê sách điện tử')
	]

	order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='orderId')
	book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookISBN')
	quantity = models.IntegerField(default=0)
	option = models.CharField(max_length=10, choices=OPTION, default='buy')

	class Meta:
		managed = False
		db_table = 'order_item'
		unique_together = (('book', 'order'))

	@property
	def subtotal(self):
		if self.option == "eRent":
			return self.quantity * self.book.rent_price
		return self.quantity * self.book.price

	def __str__(self):
		return str(self.id) + " - " + str(self.book) 

class Card(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, db_column='customerId')
	ownerName = models.CharField(max_length=50)
	code = CardNumberField(max_length=20)
	bank = models.CharField(max_length=50)
	branch = models.CharField(max_length=50, blank=True)
	expireDate = models.DateField()

	class Meta:
		managed = False
		db_table = 'card'
		unique_together = (('customer', 'code'))

	def code_mask(self):
		return self.code[:3] + "****" + self.code[-3:]

	def __str__(self):
		return str(self.id) + " - " + str(self.customer) 

class Payment(models.Model):
	PAYMENT_METHOD = [
		('credit', 'credit'),
		('transfer', 'transfer')
	]

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, db_column='customerId')
	order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='orderId')
	staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, db_column='staffId')

	paymentTime = models.DateTimeField(auto_now_add=True)
	method = models.CharField(max_length=12, choices=PAYMENT_METHOD, default='transfer')
	amount = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		managed = False
		db_table = 'payment'

	def __str__(self):
		return str(self.id) + " - " + str(self.customer) 

class Review(models.Model):
	RATING = [(i, i) for i in range(1, 6)]

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customerId')
	book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookISBN')

	reviewTime = models.DateTimeField(auto_now_add=True)
	comment = models.CharField(max_length=400)
	rating = models.IntegerField(choices=RATING)

	class Meta:
		managed = False
		db_table = 'review'
		unique_together = (('customer', 'book'))

	def __str__(self):
		return str(self.id) + " - " + str(self.book) 

class Keyword(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookISBN')
	keyword = models.CharField(max_length=20)

	class Meta:
		managed = False
		db_table = 'keyword'
		unique_together = (('book', 'keyword'))

	def __str__(self):
		return self.keyword

class Topic(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookISBN')
	name = models.CharField(max_length=20)

	class Meta:
		managed = False
		db_table = 'topic'

	def __str__(self):
		return self.name

class Book_Image(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookISBN')
	image = models.ImageField()
	# default = models.BooleanField(default=False)

	class Meta:
		managed = False
		db_table = 'book_image'
		unique_together = (('book', 'image'))

	def __str__(self):
		return str(self.book)

	def image_url(self):
		return self.image.url

class Inventory(models.Model):
	book = models.ForeignKey(Traditional, on_delete=models.CASCADE, db_column='bookISBN')
	storage = models.ForeignKey(Storage, on_delete=models.CASCADE, db_column='storageId')
	quantity = models.IntegerField()

	class Meta:
		managed = False
		db_table = 'store'
		unique_together = (('book', 'storage'))

	def __str__(self):
		return str(self.id) + " - " + str(self.book) 