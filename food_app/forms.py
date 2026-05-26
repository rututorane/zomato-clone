from django import forms 
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name','address','phone']
        widgets = {'full_name':forms.TextInput(attrs={'class': 'form-control','rows':3,'placeholder': 
        'Enter your full name'}),'address':forms.Textarea(attrs={'class':'form-control','rows':3,
        'placeholder':'Enter your delivery address'}), 'phone': forms.TextInput(attrs={'class': 
        'form-control', 'placeholder': 'Enter phone number'})
        }
   