from functools import reduce
import json
from .models import *

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		total = reduce(lambda x, y: x + y.subtotal, items, 0)

	return {'order': order, 'items': items, 'total': total}