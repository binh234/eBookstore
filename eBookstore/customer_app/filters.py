import django_filters
from django_filters import *
from django_filters.widgets import *
from django_filters.fields import *
from django import forms
from django.db import models
from django.db.models import Q

from .models import *
from functools import reduce
import time



class MultiValueCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    """
    Custom filter to accept multiple CharFilter strings provided using CSVWidget
    """
    def filter(self, qs, value):
        start = time.clock()
        values = value or []
        if not values:
            return qs
        queryset = None
        lookup = self.field_name + '__' + self.lookup_expr

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

        stop = time.clock()
        print("time:", stop-start)
        return self.get_method(qs)(query)

class OrderByFilter(filters.ChoiceFilter):
    def filter(self, qs, value):
        if value:
            return qs.order_by(value)
        else:
            return qs

class BookFilter(FilterSet):
    BOOK_ORDER_CHOICE = (
        ('name', 'Tên sách'),
        ('price', 'Giá bán'),
        ('-avg_rating', 'Đánh giá')
    )
    order = OrderByFilter(choices=BOOK_ORDER_CHOICE, label='Sắp xếp theo')

    ISBN = CharFilter(field_name='ISBN', lookup_expr='icontains', label='ISBN')
    name = CharFilter(lookup_expr='icontains', label='Tên sách')
    year = NumberFilter(label='Năm xuất bản')
    price = RangeFilter(field_name='price',widget=RangeWidget(attrs={'class': 'col'}), label='Giá')
    topic = MultiValueCharFilter(field_name='topic__name', 
        lookup_expr="icontains", 
        label="Thể loại", 
        widget=CSVWidget(),
        distinct=True, 
        help_text=None)
    keyword = MultiValueCharFilter(field_name='keyword__keyword', 
        lookup_expr="icontains", 
        label="Từ khóa", 
        widget=CSVWidget(),
        distinct=True, 
        help_text=None)
    publisher = ModelChoiceFilter(queryset=Publisher.objects.all(), label='Nhà xuất bản')
    traditional = BooleanFilter(label='Sách truyền thống')
    electronic = BooleanFilter(label='Sách điện tử')
    authors = ModelMultipleChoiceFilter(queryset=Author.objects.all(), label='Tác giả')
    # topics = ModelMultipleChoiceFilter(field_name='topic__name', queryset=Topic.objects.values("name").distinct(), label='Thể loại')

    class Meta:
        model = Book
        fields = ['order', 'ISBN', 'name', 'year', 'price', 'topic', 'keyword', 'publisher', 'traditional', 'electronic', 'authors']
        filter_overrides = {
            models.CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains'
                } 
            },
        }

    def kFilter(self, queryset, name, value):
        return queryset.filter(**{name: value})

class AuthorFilter(FilterSet):
    ORDER_AUTHOR_CHOICE = (
        ('name', 'Tên'),
        ('book_count', 'Số lượng sách'),
    )
    order = OrderByFilter(choices=ORDER_AUTHOR_CHOICE, label='Sắp xếp theo')
    topic = MultiValueCharFilter(field_name='book__topic__name', 
        lookup_expr="icontains", 
        label="Thể loại", 
        widget=CSVWidget(attrs={'class': 'col ml-2'}),
        distinct=True, 
        help_text=None)
    # topic = ModelChoiceFilter(queryset=Topic.objects.all().distinct(), label="Thể loại", method="topicFilter")
    keyword = MultiValueCharFilter(field_name='book__keyword__keyword', 
        lookup_expr="icontains", 
        label="Từ khóa", 
        widget=CSVWidget(attrs={'class': 'col ml-2'}),
        distinct=True, 
        help_text=None)

    class Meta:
        model = Author
        fields = ['topic', 'keyword', 'order']

    def topicFilter(self, queryset, name, value):
        field_name = "book__topic"
        return queryset.filter(**{field_name: value}).distinct()

class OrderItemFilter(FilterSet):
    order_date = DateFromToRangeFilter(field_name='order__orderTime', label="Thời gian mua")

    class Meta:
        model = OrderItem
        fields = ['order_date']
        

class BoughtTopicFilter(FilterSet):
    order_date = DateFromToRangeFilter(field_name='book__orderitem__order__orderTime', label="Thời gian mua")

    class Meta:
        model = Topic
        fields = ['order_date']
            