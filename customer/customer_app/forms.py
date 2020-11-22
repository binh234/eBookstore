from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class RegisterForm(UserCreationForm):
	email = forms.CharField(required=True)
	class Meta:
		model = User
		fields = ['email', 'username', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data.get("email")

		if Customer.objects.filter(email=email):
			raise forms.ValidationError("""Email đã được sử dụng bởi một tài khoản khác""",code='duplicate_email')
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		errors = []
		if len(password2) < 8:
			errors.append(forms.ValidationError("""Mật khẩu phải có ít nhất 8 kí tự""",code='short_password'))
		if password2.isdigit() or password1.isdigit():
			errors.append(forms.ValidationError("""Mật khẩu phải chứa ít nhật 1 kí tự chữ""",code='numeric_password'))
		if password2 != password1:
			errors.append(forms.ValidationError("""Mật khẩu không trùng khớp""",code='password_mismatch'))

		if errors:
			raise forms.ValidationError(errors)
		else:
			return password2

class CustomerForm(ModelForm):
	firstName = forms.CharField(label='Họ và tên đệm')
	lastName = forms.CharField(label='Tên')
	phone = forms.CharField(label='Số điện thoại', required=False)
	address = forms.CharField(label='Địa chỉ', required=False)
	avatar = forms.ImageField(label='Ảnh đại diện')
	
	class Meta:
		model = Customer
		fields = "__all__"
		exclude = ['user']

class CardForm(ModelForm):
	ownerName = forms.CharField(label='Chủ thẻ')
	code = forms.CharField(label='Mã thẻ')
	expireDate = forms.CharField(label='Ngày hết hạn', widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))
	bank = forms.CharField(label='Ngân hàng')
	branch = forms.CharField(label='Chi nhánh')

	class Meta:
		model = Card
		fields = "__all__"
		exclude = ['customer']
			