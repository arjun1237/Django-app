from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# create your views here
from .models import *
from .forms import OrderForm, UserRegForm
from .filters import order_filter

@login_required(login_url='login')
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

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Incorrect Credentials')
	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	form = UserRegForm()
	if request.method == 'POST':
		form = UserRegForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products' : products})

@login_required(login_url='login')
def customer(request, pk_cust_id):
	customer = Customer.objects.get(id=pk_cust_id)
	orders = customer.order_set.all()	
	orders_count = orders.count()
	
	my_filter = order_filter(request.GET, queryset=orders)
	orders = my_filter.qs
	context = {'customer': customer, 'orders': orders, 'orders_count': orders_count, 'my_filter': my_filter}
	return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def create_order(request, pk_cust_id):
	order_form_set = inlineformset_factory(Customer, Order, fields= ('product', 'status'), extra=5)
	customer = Customer.objects.get(id = pk_cust_id)
	# form = order_form(initial= {'customer': customer})
	formset = order_form_set(queryset=Order.objects.none(), instance=customer)
	if request.method == 'POST':
		# form = order_form(request.POST)
		formset = order_form_set(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context = {'formset': formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def update_order(request, pk_order_id):
	order = Order.objects.get(id = pk_order_id)
	form = OrderForm(instance = order)
	if request.method == 'POST':
		# form = order_form(request.POST, instance = order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def delete_order(request, pk_order_id):
	order = Order.objects.get(id = pk_order_id)
	context = {'item': order}
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	return render(request, 'accounts/delete.html', context)