from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import *
from django.core.paginator import Paginator
from .models import *

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def comma_split(string):
    return set(map(str.strip, string.split(",")))


def get_date_range(date, option):
    if option == "date":
        start_day = datetime.strptime(date, "%Y-%m-%d")
        end_day = start_day + timedelta(days=1)
    elif option == "month":
        start_day = datetime.strptime(date, "%Y-%m")
        start_day = start_day.replace(day=1)
        end_day = start_day + relativedelta(months=1)
    return [start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")]


def get_buy_item(date_range):
    return OrderItem.objects.filter(
        Q(option="buy") | Q(option="eBuy"),
        order__complete=True,
        order__orderTime__range=date_range,
    )


def get_rent_item(date_range):
    return OrderItem.objects.filter(
        option="eRent", order__complete=True, order__orderTime__range=date_range
    )


def get_all_item(date_range):
    return OrderItem.objects.filter(
        order__complete=True, order__orderTime__range=date_range
    ).annotate(number=Case(When(option="eRent", then=1), default="quantity"))


def save_import(request, form, form_temp, list_temp):
    data = {}
    if request.method == "POST":
        if form.is_valid():
            staff = request.user.staff
            item = form.save(commit=False)
            item.staff = staff
            item.storage = staff.storage
            item.save()
            data["form_is_valid"] = True
            import_history = (
                Import.objects.filter(staff=staff)
                .select_related("book__book")
                .order_by("-importTime")
            )

            data["list"] = render_to_string(
                list_temp,
                {
                    "import_obj": import_history,
                },
            )
        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(form_temp, context, request=request)

    return JsonResponse(data)


def save_export(request, form, form_temp, list_temp):
    data = {}
    if request.method == "POST":
        if form.is_valid():
            staff = request.user.staff
            item = form.save(commit=False)
            item.staff = staff
            item.storage = staff.storage
            item.save()
            data["form_is_valid"] = True
            export_history = (
                Export.objects.filter(staff=staff)
                .select_related("book__book")
                .order_by("-exportTime")
            )

            data["list"] = render_to_string(
                list_temp,
                {
                    "export_obj": export_history,
                },
            )
        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(form_temp, context, request=request)

    return JsonResponse(data)


def save_error_payment(request, form, form_temp, list_temp):
    data = {}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            error_payment_list = Payment.objects.exclude(
                status="finish"
            ).select_related("customer")

            data["list"] = render_to_string(
                list_temp,
                {
                    "error_payment_list": error_payment_list,
                },
            )
        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(form_temp, context, request=request)

    return JsonResponse(data)


def save_author(request, form, form_temp, list_temp):
    data = {}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            author_list = (
                Author.objects.all()
                .exclude(book__orderitem__order__complete=False)
                .annotate(
                    book_count=Sum(
                        Case(
                            When(book__orderitem__option="eRent", then=1),
                            default="book__orderitem__quantity",
                        )
                    )
                )
                .order_by("id")
                .values("id", "name", "email", "book_count")
            )

            paginator = Paginator(author_list, 8)  # Show 25 contacts per page.

            page_obj = paginator.get_page("1")

            data["list"] = render_to_string(list_temp, {"page_obj": page_obj})
        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(form_temp, context, request=request)

    return JsonResponse(data)


def save_book(request, form, form_temp, list_temp):
    data = {}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            book_list = (
                Book.objects.all()
                .order_by("name")
                .select_related("publisher")
                .prefetch_related("authors")
            )

            paginator = Paginator(book_list, 12)  # Show 25 contacts per page.

            page_obj = paginator.get_page("1")

            data["list"] = render_to_string(list_temp, {"page_obj": page_obj})
        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(form_temp, context, request=request)

    return JsonResponse(data)
