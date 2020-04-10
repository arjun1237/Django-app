from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import order_form

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

def customer(request, pk_cust_id):
	customer = Customer.objects.get(id=pk_cust_id)
	orders = customer.order_set.all()
	orders_count = orders.count()
	context = {'customer': customer, 'orders': orders, 'orders_count': orders_count}
	return render(request, 'accounts/customer.html', context)

def create_order(request, pk_cust_id):
	order_form_set = inlineformset_factory(Customer, Order, fields= ('product', 'status'), extra=3)
	customer = Customer.objects.get(id = pk_cust_id)
	# form = order_form(initial= {'customer': customer})
	formset = order_form_set(instance=customer)
	if request.method == 'POST':
		# form = order_form(request.POST)
		formset = order_form_set(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context = {'formset': formset}
	return render(request, 'accounts/order_form.html', context)

def update_order(request, pk_order_id):
	order = Order.objects.get(id = pk_order_id)
	form = order_form(instance = order)
	if request.method == 'POST':
		# form = order_form(request.POST, instance = order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)

def delete_order(request, pk_order_id):
	order = Order.objects.get(id = pk_order_id)
	context = {'item': order}
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	return render(request, 'accounts/delete.html', context)