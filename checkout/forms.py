from django import forms
from .models import CustomerPaymentDetails

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CustomerPaymentDetails
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'city',
            'state',
            'zip_code',
            'payment_method'
        ]    

