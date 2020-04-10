from django.forms import ModelForm
from .models import *

class order_form(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'