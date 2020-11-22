"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
	path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
	path('shop/', shop, name='shop'),
    path('shop/<str:pk>/', book_detail, name='book_detail'),

    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),

    path('order/', order, name='order'),

    path('author/', author, name='author'),
    path('author/<str:pk>/', authorBookList, name='author-book-list'),

    path('bought-book/', boughtBook, name='bought-book'),
    path('bought-book-by-topic/', boughtBookByTopic, name='bought-book-by-topic'),

    path('profile/', profile, name='profile'),
    path('card/', cardList, name='card-list'),
    path('card/insert/', cardInsert, name='card-insert'),
    path('card/<str:pk>/delete/', cardDelete, name='card-delete'),
    path('card/<str:pk>/update/', cardUpdate, name='card-update'),
    path('change-password/', changePassword, name='change-password'),

	path('update-item/', updateItem, name='update-item'),
    path('process-order/', processOrder, name='process-order'),
]