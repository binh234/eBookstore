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
	path('', dashboard, name='dashboard'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
	path('im-export/', im_export, name='im_export'),
	path('import/create', import_create, name='import_create'),
	path('import/<int:pk>/update/', import_update, name='import_update'),
	path('export/create', export_create, name='export_create'),
	path('export/<int:pk>/update/', export_update, name='export_update'),
	path('error_transaction/', error_transaction, name='error_transaction'),
	path('error_transaction/<int:pk>/update', process_error_transaction, name='error_update'),
	path('author/', author, name='author'),
	path('author/create', author_create, name='author_create'),
	path('author/<int:pk>/update/', author_update, name='author_update'),

	path('storage/', storage, name='storage'),
	path('book/', book, name='book'),
	path('book/create', book_create, name='book_create'),
	path('book/<str:pk>/update', book_update, name='book_update'),
	path('order/', order, name='order'),
	path('order/<int:pk>/', order_detail, name='order_detail'),
	path('order/<int:pk>/export', export_order, name='order_export'),
	path('order/<int:pk>/cancel', cancel_order, name='order_cancel'),
	path('payment/', payment, name='payment'),
	path('profile/', profile, name='profile'),
]