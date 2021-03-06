from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.loginPage, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.logoutUser, name='logout'),

	path('', views.home, name='home'),
	path('products/', views.products, name='products'),
	path('customer/<int:pk_cust_id>/', views.customer, name='customer'),
	path('create_order/<int:pk_cust_id>', views.create_order, name='create_order'),
	path('update_order/<int:pk_order_id>', views.update_order, name='update_order'),
	path('delete_order/<int:pk_order_id>', views.delete_order, name='delete_order')
]