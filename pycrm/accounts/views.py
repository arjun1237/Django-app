from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request):
	orders = Order.objects.all()
	orders_top5 = orders.order_by('status')[:5]
	customers = Customer.objects.all()
	total_cust = customers.count()
	total_ord = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()


	context = {'orders': orders_top5, 'customers': customers,
	'total_ord': total_ord, 'total_cust': total_cust,
	'delivered': delivered, 'pending': pending
	}
	return render(request, 'accounts/dashboard.html', context)

def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products' : products})

def customer(request):
	return render(request, 'accounts/customer.html')