from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Keyword)
admin.site.register(Inventory)
admin.site.register(Import)
admin.site.register(Export)
admin.site.register(Book)
admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book_Image)
admin.site.register(BookAuthor)

