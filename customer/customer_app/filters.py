from django_filters import *
from django_filters.widgets import *
from django_filters.fields import *
from django import forms
from django.db import models
from django.db.models import Q

from .models import *


class MultiValueCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        values = value or []
        if not values:
            return qs
        lookup = self.field_name + "__" + self.lookup_expr

        if self.distinct:
            qs = qs.distinct()
        query = Q()
        for value in values:
            if value in EMPTY_VALUES:
                return qs
            # if not queryset:
            #     queryset = self.get_method(qs)(**{lookup: value})
            # else:
            #     queryset = queryset | self.get_method(qs)(**{lookup: value})
            query |= Q(**{lookup: value})

        return self.get_method(qs)(query)


class BooleanForeignFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if value is not None:
            lookup = self.field_name + "__" + self.lookup_expr
            value = not value
            print(lookup, value)
            return self.get_method(qs)(**{lookup: value})
        else:
            return qs


class OrderByFilter(filters.ChoiceFilter):
    def filter(self, qs, value):
        if value:
            return qs.order_by(value)
        else:
            return qs


class BookFilter(FilterSet):
    BOOK_ORDER_CHOICE = (
        ("name", "Tên sách"),
        ("price", "Giá bán"),
        ("-avg_rating", "Đánh giá"),
    )
    order = OrderByFilter(choices=BOOK_ORDER_CHOICE, label="Sắp xếp theo")

    ISBN = CharFilter(field_name="ISBN", lookup_expr="icontains", label="ISBN")
    name = CharFilter(lookup_expr="icontains", label="Tên sách")
    year = NumberFilter(label="Năm xuất bản")
    price = RangeFilter(
        field_name="price", widget=RangeWidget(attrs={"class": "col"}), label="Giá"
    )
    topic = MultiValueCharFilter(
        field_name="topic__name",
        lookup_expr="icontains",
        label="Thể loại",
        widget=CSVWidget(),
        distinct=True,
        help_text=None,
    )
    keyword = MultiValueCharFilter(
        field_name="keyword__keyword",
        lookup_expr="icontains",
        label="Từ khóa",
        widget=CSVWidget(),
        distinct=True,
        help_text=None,
    )
    publisher = ModelChoiceFilter(
        queryset=Publisher.objects.all(), label="Nhà xuất bản"
    )
    traditional = BooleanForeignFilter(
        field_name="traditional", lookup_expr="isnull", label="Sách truyền thống"
    )
    electronic = BooleanForeignFilter(
        field_name="electronic", lookup_expr="isnull", label="Sách điện tử"
    )
    authors = ModelMultipleChoiceFilter(queryset=Author.objects.all(), label="Tác giả")
    # topics = ModelMultipleChoiceFilter(field_name='topic__name', queryset=Topic.objects.values("name").distinct(), label='Thể loại')

    class Meta:
        model = Book
        fields = [
            "order",
            "ISBN",
            "name",
            "year",
            "price",
            "topic",
            "keyword",
            "publisher",
            "traditional",
            "electronic",
            "authors",
        ]
        filter_overrides = {
            models.CharField: {
                "filter_class": CharFilter,
                "extra": lambda f: {"lookup_expr": "icontains"},
            },
        }

    def kFilter(self, queryset, name, value):
        return queryset.filter(**{name: value})


class AuthorFilter(FilterSet):
    ORDER_AUTHOR_CHOICE = (
        ("name", "Tên"),
        ("book_count", "Số lượng sách"),
    )
    order = OrderByFilter(choices=ORDER_AUTHOR_CHOICE, label="Sắp xếp theo")
    topic = MultiValueCharFilter(
        field_name="book__topic__name",
        lookup_expr="icontains",
        label="Thể loại",
        widget=CSVWidget(attrs={"class": "col ml-2"}),
        distinct=True,
        help_text=None,
    )
    # topic = ModelChoiceFilter(queryset=Topic.objects.all().distinct(), label="Thể loại", method="topicFilter")
    keyword = MultiValueCharFilter(
        field_name="book__keyword__keyword",
        lookup_expr="icontains",
        label="Từ khóa",
        widget=CSVWidget(attrs={"class": "col ml-2"}),
        distinct=True,
        help_text=None,
    )

    class Meta:
        model = Author
        fields = ["topic", "keyword", "order"]

    def topicFilter(self, queryset, name, value):
        field_name = "book__topic"
        return queryset.filter(**{field_name: value}).distinct()


class OrderItemFilter(FilterSet):
    order_date = DateFromToRangeFilter(
        field_name="order__orderTime",
        label="Ngày mua",
        widget=RangeWidget(attrs={"type": "date"}),
    )

    class Meta:
        model = OrderItem
        fields = ["order_date"]


class OrderFilter(FilterSet):
    BOOK_CHOICE = (("both", "Cả sách điện tử và truyền thống"),)
    ORDER_BY_CHOICE = (
        ("-orderTime", "Thời gian đặt hàng"),
        ("-book_count", "Số lượng sách"),
    )

    order_date = DateFromToRangeFilter(
        field_name="orderTime",
        label="Ngày đặt hàng",
        widget=RangeWidget(attrs={"type": "date"}),
    )
    status = MultipleChoiceFilter(
        field_name="status",
        choices=Order.ORDER_STATUS,
        label="Trạng thái",
        widget=forms.CheckboxSelectMultiple(),
    )
    book_type = ChoiceFilter(
        field_name="orderitem__option",
        choices=BOOK_CHOICE,
        label="Loại sách",
        method="bookFilter",
    )
    order = OrderByFilter(choices=ORDER_BY_CHOICE, label="Sắp xếp theo")

    class Meta:
        model = Order
        fields = ["order_date", "book_type", "order", "status"]

    def bookFilter(self, queryset, name, value):
        if value is None:
            return queryset
        elif value == "both":
            subquery = OrderItem.objects.filter(~Q(option="buy")).values_list(
                "order_id", flat=True
            )

        return queryset.filter(**{name: "buy"}, id__in=subquery).distinct()
