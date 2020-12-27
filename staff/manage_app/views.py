from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required

import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import *
from .forms import *
from .utils import *
from .decorators import *

# Create your views here.
def login_page(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			# messages.success(request, "Đăng nhập thành công")
			return redirect("dashboard")
		else:
			pass
			# messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác")

	context = {}
	return render(request, 'login/login.html', context)

def logout_page(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@staff_only
def dashboard(request):
	select_date = request.GET.get("date")
	if select_date:
		option = "date" if select_date.count("-") == 2 else "month"
		date_range = get_date_range(select_date, option)
	else:
		option = "date"
		start_day = datetime.today()
		end_day = start_day + timedelta(days=1)
		select_date = start_day.strftime("%Y-%m-%d")
		date_range = [select_date, end_day.strftime("%Y-%m-%d")]

	item_list = get_buy_item(date_range
	).values("book__ISBN", "book__name", "book__price").annotate(
	book_count=Sum("quantity")
	)
	top_item_list = item_list.order_by("-book_count")[:5]

	total_eRent = get_rent_item(date_range).count()
	total_buy = item_list.filter(option='buy').aggregate(total=Sum('book_count'))['total']
	total_eBuy = item_list.filter(option='eBuy').aggregate(total=Sum('book_count'))['total']
	category = "ngày" if option == "date" else "tháng"

	if total_buy is None:
		total_buy = 0
	if total_eBuy is None:
		total_eBuy = 0

	context = {
		'item_list': item_list,
		'top_item_list': top_item_list,
		'total_book': total_buy + total_eBuy,
		'total_buy': total_buy,
		'total_eBuy': total_eBuy,
		'total_eRent': total_eRent,
		'select_date': select_date,
		'option': (option=='date'),
		'category': category,
	}
	return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
@staff_only
def im_export(request):
	staff = request.user.staff
	import_history = Import.objects.filter(staff=staff).select_related("book__book").order_by("-importTime")
	export_history = Export.objects.filter(staff=staff).select_related("book__book").order_by("-exportTime")

	context = {
		"import_obj": import_history,
		"export_obj": export_history,
	}
	return render(request, 'im_export/im-export.html', context)

@login_required(login_url='login')
@staff_only
def import_create(request):
	form = ImportForm(request.POST or None)
	form_temp = 'im_export/import_form.html'
	list_temp = 'im_export/import_item.html'

	return save_import(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def import_update(request, pk):
	item = get_object_or_404(Import, id=pk)
	if request.method == "POST":
		form = ImportForm(request.POST, instance=item)
	else:
		form = ImportForm(instance=item)
	form_temp = 'im_export/import_form.html'
	list_temp = 'im_export/import_item.html'

	return save_import(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def export_create(request):
	form = ExportForm(request.POST or None)
	form_temp = 'im_export/export_form.html'
	list_temp = 'im_export/export_item.html'

	return save_export(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def export_update(request, pk):
	item = get_object_or_404(Export, id=pk)
	if request.method == "POST":
		form = ExportForm(request.POST, instance=item)
	else:
		form = ExportForm(instance=item)

	form_temp = 'im_export/export_form.html'
	list_temp = 'im_export/export_item.html'

	return save_export(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def error_transaction(request):
	error_payment_list = Payment.objects.exclude(status='finish').select_related('customer')

	context = {
		'error_payment_list': error_payment_list,
	}
	return render(request, 'error/error-transaction.html', context)

@login_required(login_url='login')
@staff_only
def process_error_transaction(request, pk):
	payment = get_object_or_404(Payment, id=pk)
	form = ErrorPaymentForm(request.POST or None, instance=payment)
	form_temp = 'error/error_form.html'
	list_temp = 'error/error_item.html'
	return save_error_payment(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def author(request):
	if request.method == "GET":
		start_day = datetime.today()
		end_day = start_day + timedelta(days=1)
		next_month = start_day + relativedelta(months=1)
		date_range = [start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")]
		month_range = [start_day.replace(day=1).strftime("%Y-%m-%d"), next_month.replace(day=1).strftime("%Y-%m-%d")]

		top_author_day = get_buy_item(date_range
		).values("book__authors__id", "book__authors__name", "book__authors__email").annotate(
		book_count=Sum("quantity")
		).order_by("-book_count")[:5]
		top_author_month = get_buy_item(month_range
		).values("book__authors__id", "book__authors__name", "book__authors__email").annotate(
		book_count=Sum("quantity")
		).order_by("-book_count")[:5]

		author_list = Author.objects.all().exclude(book__orderitem__order__complete=False).annotate(
			book_count=Sum(Case(
				When(book__orderitem__option='eRent', then=1),
				default='book__orderitem__quantity'
			))).order_by("id").values("id", "name", "email", "book_count")

		paginator = Paginator(author_list, 8) # Show 25 contacts per page.

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		context = {
			'page_obj': page_obj,
			'top_day': top_author_day,
			'top_month': top_author_month,
			'cur_date': start_day.strftime("%Y-%m-%d"),
			'cur_month': start_day.strftime("%Y-%m"),
		}
		return render(request, 'author/author.html', context)
	else:
		data = {}
		option = request.POST.get("option")
		date = request.POST.get("date")
		date_range = get_date_range(date, option)
		top_author = get_buy_item(date_range
		).values("book__authors__id", "book__authors__name", "book__authors__email").annotate(
		book_count=Sum("quantity")
		).order_by("-book_count")[:5]
		data['form_is_valid'] = True
		data['list'] = render_to_string('author/top_author_item.html',{'top_author': top_author})
		return JsonResponse(data)

@login_required(login_url='login')
@staff_only
def author_create(request):
	form = AuthorForm(request.POST or None)
	form_temp = 'author/author_form.html'
	list_temp = 'author/author_item.html'

	return save_author(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def author_update(request, pk):
	author = get_object_or_404(Author, id=pk)
	form = AuthorForm(request.POST or None, instance=author)
	form_temp = 'author/author_form.html'
	list_temp = 'author/author_item.html'

	return save_author(request, form, form_temp, list_temp)

@login_required(login_url='login')
@staff_only
def storage(request):
	if request.method == "GET":
		start_day = datetime.today().replace(day=1)
		end_day = start_day + relativedelta(months=1)
		date_range = [start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")]
		top_export = Storage.objects.filter(export__exportTime__range=date_range
			).annotate(export_num=Sum("export__quantity")).order_by("-export_num")[:5]

		storage = request.user.staff.storage
		item_list = Inventory.objects.filter(storage=storage).order_by("quantity").select_related("book__book")

		lack_item_list = Inventory.objects.filter(storage=storage, quantity__lt=10).order_by("quantity").select_related("book__book")

		context = {
			'top_export': top_export,
			'item_list': item_list,
			'lack_item_list': lack_item_list,
			'cur_month': start_day.strftime("%Y-%m"),
		}
		return render(request, 'storage/storage.html', context)
	else:
		data = {}
		date = request.POST.get("date")
		date_range = get_date_range(date, "month")
		top_export = Storage.objects.filter(export__exportTime__range=date_range
			).annotate(export_num=Sum("export__quantity")).order_by("-export_num")[:5]
		data['form_is_valid'] = True
		data['list'] = render_to_string('storage/top_storage_item.html',{'top_export': top_export})
		return JsonResponse(data)

@login_required(login_url='login')
@staff_only
def book(request):
	book_list = Book.objects.all().order_by("name").select_related("publisher").prefetch_related("authors")

	paginator = Paginator(book_list, 12) # Show 25 contacts per page.

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
	}
	return render(request, 'book/book.html', context)

@login_required(login_url='login')
@staff_only
def book_create(request):
	form = BookForm(request.POST or None, request.FILES or None)

	if request.method == "POST":
		if form.is_valid():
			book = form.save()
			form.save_extra(book)
			return redirect("book")

	context = {
		'form': form,
	}

	return render(request, 'book/book_create.html', context)

@login_required(login_url='login')
@staff_only
def book_update(request, pk):
	book = get_object_or_404(Book, ISBN=pk)
	form = BookForm(request.POST or None, request.FILES or None, instance=book)

	if request.method == "POST":
		if form.is_valid():
			book = form.save()
			form.save_extra(book)
			return redirect("book")

	context = {
		'form': form,
	}

	return render(request, 'book/book_create.html', context)

@login_required(login_url='login')
@staff_only
def order(request):
	staff = request.user.staff
	order_list = Order.objects.filter(Q(staff=staff)|Q(staff__isnull=True), 
		complete=True).order_by("-orderTime").select_related("customer").prefetch_related("orderitem_set")

	paginator = Paginator(order_list, 8) # Show 25 contacts per page.

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
	}
	return render(request, 'order/order.html', context)

@login_required(login_url='login')
@staff_only
def order_detail(request, pk):
	order = get_object_or_404(Order, id=pk)
	item_list = order.orderitem_set.all().select_related("book")

	context = {
		'order': order,
		'item_list': item_list,
	}
	return render(request, 'order/order_detail.html', context)

@login_required(login_url='login')
@staff_only
def cancel_order(request, pk):
	order = get_object_or_404(Order, id=pk)
	if order.can_cancel:
		order.status = "Cancel"
		order.save()

		return redirect('order')

@login_required(login_url='login')
@staff_only
def export_order(request, pk):
	staff = request.user.staff
	storage = staff.storage
	order = get_object_or_404(Order, id=pk)

	if order.can_export:
		item_list = order.orderitem_set.all().select_related("book")

		for item in item_list:
			if item.option == "buy":
				book = item.book.traditional
				export_item = Export(book=book, staff=staff, storage=storage, quantity=item.quantity)
				export_item.save()
		order.status = "Delivered"
		order.save()

		return redirect('order')

@login_required(login_url='login')
@staff_only
def payment(request):
	if request.method == "GET":
		start_day = datetime.today()
		end_day = start_day + timedelta(days=1)
		date_range = [start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")]
		card_payment_list = Payment.objects.filter(method='credit', 
			paymentTime__range=date_range).select_related('customer')
		error_payment_list = Payment.objects.filter(method='credit').exclude(status='finish').select_related('customer')

		context = {
			'card_payment_list': card_payment_list,
			'error_payment_list': error_payment_list,
			'cur_date': start_day.strftime("%Y-%m-%d")
		}
		return render(request, 'payment/payment.html', context)
	else:
		data = {}
		date = request.POST.get("date")
		date_range = get_date_range(date, "date")
		card_payment_list = Payment.objects.filter(method='credit', 
			paymentTime__range=date_range).select_related('customer')
		data['form_is_valid'] = True
		data['list'] = render_to_string('payment/payment_item.html',{'card_payment_list': card_payment_list,})
		return JsonResponse(data)

@login_required(login_url='login')
@staff_only
def profile(request):
	staff = request.user.staff
	if request.method == "POST":
		form = StaffForm(request.POST, request.FILES, instance=staff)
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = StaffForm(instance=staff)

	context = {
		'form': form,
		'staff': staff,
	}
	return render(request, 'profile/profile.html', context)