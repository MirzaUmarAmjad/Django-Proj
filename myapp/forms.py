from django import forms
from myapp.models import Order, Student


class InterestForm(forms.Form):
    interested = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices=((1,"Yes"),(0,"No")),label="Interested")
    levels = forms.IntegerField(initial=1, min_value=1, label="Levels")
    comments = forms.CharField(widget=forms.Textarea, label="Additional Comments", required= False)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student','course','levels','order_date']
        widgets = {'student': forms.RadioSelect(), 'order_date':forms.SelectDateWidget()}

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_photo','username', 'password', 'first_name', 'last_name', 'email','school']
        # widgets = {'student': forms.RadioSelect(), 'order_date': forms.SelectDateWidget()}

class ForgotPassswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Username")
