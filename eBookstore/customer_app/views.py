from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.db.models import *

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import json
import datetime
from decimal import Decimal

from .models import *
from .filters import *
from .utils import cartData
from .forms import *
from .decorators import *

# Create your views here.
@unauthenticated_user
def login_page(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			messages.success(request, "Đăng nhập thành công")
			return redirect("home")
		else:
			messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác")
			# return redirect("home")

	context = {}
	return render(request, 'login/login.html', context)

@unauthenticated_user
def register_page(request):
	form = RegisterForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(name="customer")
			user.groups.add(group)

			email = request.POST.get("email")
			name = request.POST.get("name")
			customer = Customer.objects.create(user=user, email=email, name=name)

			messages.success(request, "Đăng ký tài khoản thành công")
			return redirect('login')
		else:
			for field in form:
				if field.errors:
					for error in field.errors:
						messages.error(request, error)

	context = {
		'form': form,
	}
	return render(request, 'login/register.html', context)

def logout_page(request):
	logout(request)
	return redirect('home')

def home(request):
	best_seller = Book.objects.annotate(sale=Sum("orderitem__quantity")).order_by("-sale")[:6]
	recommend_book = Book.objects.annotate(avg_rating=Avg("review__rating")).order_by("-avg_rating")[:10]

	context = {
		"best_seller": best_seller,
		"recommend": recommend_book,
	}
	return render(request, 'customer/home.html', context)

def shop(request):
	book_list = Book.objects.all()
	book_filter = BookFilter(request.GET, queryset=book_list)

	book_list = book_filter.qs
	book_list = book_list.annotate(avg_rating=Avg("review__rating"))

	paginator = Paginator(book_list, 12) # Show 25 contacts per page.

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	# print(object_filter.form)

	context = {
		'page_obj': page_obj,
		'object_count': book_list.count(),
		'filter': book_filter,
	}
	return render(request, 'customer/shop.html', context)

def book_detail(request, pk):
	book_query = Book.objects.annotate(
		total_rating=Count("review"),
		avg_rating=Avg("review__rating")
		).select_related("traditional", "electronic", "publisher")
	book = get_object_or_404(book_query, ISBN=pk)

	book_author = book.authors.all()
	same_author = Book.objects.filter(~Q(ISBN=book.ISBN), authors__in=book_author)[:6]

	book_topic = book.topic_set.values_list('name', flat=True)
	same_topic = Book.objects.filter(~Q(ISBN=book.ISBN), topic__name__in=book_topic)[:6]

	context = {
		'object': book,
		'same_author': same_author,
		'same_topic': same_topic,
	}
	return render(request, 'customer/book_detail.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
	data = cartData(request)
	order = data['order']
	items = data['items']
	total = data['total']

	context = {
		"order": order,
		"items": items,
		"total": total,
	}
	return render(request, 'customer/cart.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
	data = cartData(request)
	order = data['order']
	items = data['items']
	total = data['total']

	context = {
		"order": order,
		"items": items,
		"total": total,
		"shipping": order.shipping,
	}
	return render(request, 'customer/checkout.html', context)

def author(request):
	author_list = Author.objects.all()
	author_filter = AuthorFilter(request.GET, queryset=author_list)
	author_list = author_filter.qs
	author_list = author_list.annotate(book_count=Count("book")).values("id", "name", "book_count")

	paginator = Paginator(author_list, 10) # Show 10 authors per page.

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'filter': author_filter,
	}
	return render(request, 'customer/author.html', context)

def authorBookList(request, pk):
	author = get_object_or_404(Author, id=pk)
	book_list = Book.objects.filter(authors__id=pk)

	paginator = Paginator(book_list, 12) # Show 25 contacts per page.

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'author': author,
		'page_obj': page_obj,
		'object_count': book_list.count(),
	}

	return render(request, 'customer/author_book_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def boughtBook(request):
	customer = request.user.customer
	item_list = OrderItem.objects.filter(Q(option='buy')|Q(option='eBuy'), 
	order__customer=customer,
	order__complete=True)
	item_filter = OrderItemFilter(request.GET, queryset=item_list)
	item_list = item_filter.qs
	book_list = item_list.values("book", "book__name", "book__year").annotate(
	book_count=Sum("quantity"))
	
	paginator = Paginator(book_list, 10) # Show 10 contacts per page.

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
	}
	return render(request, 'customer/bought_book.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def boughtBookByTopic(request):
	customer = request.user.customer

	item_list = OrderItem.objects.filter(Q(option='buy')|Q(option='eBuy'), 
	order__customer=customer,
	order__complete=True)
	item_filter = OrderItemFilter(request.GET, queryset=item_list)
	item_list = item_filter.qs
	topic_list = item_list.values("book__topic__name").annotate(book_count=Sum("quantity"))

	paginator = Paginator(topic_list, 10) # Show 10 contacts per page.
	print(topic_list.query)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'filter':item_filter,
	}
	return render(request, 'customer/bought_book_topic.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profile(request):
	customer = request.user.customer

	if request.method == "POST":
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
	else:
		form = CustomerForm(instance=customer)
	context = {
		'form': form,
	}
	return render(request, 'customer/profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cardList(request):
	customer = request.user.customer
	card_list = customer.card_set.all()
	context = {
		'page_obj': card_list,
	}
	return render(request, 'customer/card_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cardUpdate(request, pk):
	card = Card.objects.get(id=pk)
	if request.method == "POST":
		form = CardForm(request.POST, instance=card)
		if form.is_valid():
			form.save()
			return redirect("card-list") 
	else:
		form = CardForm(instance=card) 
	context = {
		'form': form,
	}
	return render(request, 'customer/card_update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cardInsert(request):
	if request.method == "POST":
		form = CardForm(request.POST)
		if form.is_valid():
			card = form.save()

			customer = request.user.customer
			card.customer = customer
			card.save()
			return redirect("card-list") 
	else:
		form = CardForm() 

	context = {
		'form': form,
	}
	return render(request, 'customer/card_update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cardDelete(request, pk):
	card = Card.objects.get(id=pk)
	card.delete()
	return redirect("card-list") 

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def changePassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  
			messages.success(request, 'Cập nhật mật khẩu thành công')
			return redirect('change-password')
		else:
			messages.error(request, 'Có lỗi xảy ra')
	else:
		form = PasswordChangeForm(request.user)

	context = {
		'form': form,
	}
	return render(request, 'customer/change_password.html', context)

@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	quantity = 1
	if data['quantity']:
		quantity = int(data['quantity'])
	if quantity == 0:
		quantity = 1
	option = data['option']

	customer = request.user.customer
	book = get_object_or_404(Book, ISBN=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	
	if action == 'remove':
		changed, message = order.remove_item(productId, option)
	else:
		changed, message = order.add_item(productId, quantity, option, action)

	response = {
		'message': message,
		'changed': changed,
	}
		
	return JsonResponse(response, safe=False)

@login_required(login_url='login')
def processOrder(request):
	data = json.loads(request.body)
	shipping_address = data['form']['address']
	payment_option = data['form']['option']
	shipping = bool(data['form']['shipping'])

	total = data['form']['total']
	total = float(total.replace(",", "."))
	print(total)

	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	order.complete = True
	order.orderTime = datetime.now()
	if shipping == True:
		order.shippingAddress = shipping_address

	if payment_option == "card":
		method = "credit"
	else:
		method = "transfer"

	Payment.objects.create(customer=customer, order=order, method=method, amount=total)

	order.save()

	return JsonResponse("Payment was completed", safe=False)