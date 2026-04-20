from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .models import CustomerPaymentDetails
import re


class CheckoutForm(forms.ModelForm):
    """
    Form for checkout with enhanced email validation.
    Ensures all user-entered email addresses are valid before submission.
    Uses Razorpay as the only available payment method (required selection).
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'type': 'email'
        }),
        validators=[EmailValidator(message="Please enter a valid email address (e.g., user@example.com)")],
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address (e.g., user@example.com).'
        }
    )
    
    payment_method = forms.ChoiceField(
        choices=[('razorpay', 'Razorpay - Card, Net Banking, Wallets')],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'required': True
        }),
        required=True,
        initial='razorpay',
        error_messages={
            'required': 'Please select a payment method to proceed.'
        }
    )
    
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
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city',
                'required': True
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your state',
                'required': True
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your ZIP code (5-6 digits)',
                'pattern': r'\d{5,6}',
                'required': True
            })
        }
    
    def clean_email(self):
        """
        Validate email format using Django's built-in validator
        and additional custom validation.
        """
        email = self.cleaned_data.get('email')
        
        # Handle None value
        if email is None:
            email = ''
        else:
            email = str(email).strip()
        
        # Check if email is empty
        if not email:
            raise ValidationError("Email address is required.")
        
        # Check email format with regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError(
                "Please enter a valid email address (e.g., user@example.com). "
                "Email must contain @ and a domain."
            )
        
        return email
    
    def clean_zip_code(self):
        """Validate ZIP code format."""
        zip_code = self.cleaned_data.get('zip_code')
        
        # Handle None value
        if zip_code is None:
            zip_code = ''
        else:
            zip_code = str(zip_code).strip()
        
        if not zip_code:
            raise ValidationError("ZIP code is required.")
        
        # Check if zip code is 5-6 digits
        if not re.match(r'^\d{5,6}$', zip_code):
            raise ValidationError("ZIP code must be 5-6 digits.")
        
        return zip_code
    
    def clean_first_name(self):
        """Validate first name."""
        first_name = self.cleaned_data.get('first_name')
        
        # Handle None value
        if first_name is None:
            first_name = ''
        else:
            first_name = str(first_name).strip()
        
        if not first_name:
            raise ValidationError("First name is required.")
        
        if len(first_name) < 2:
            raise ValidationError("First name must be at least 2 characters long.")
        
        return first_name
    
    def clean_last_name(self):
        """Validate last name."""
        last_name = self.cleaned_data.get('last_name')
        
        # Handle None value
        if last_name is None:
            last_name = ''
        else:
            last_name = str(last_name).strip()
        
        if not last_name:
            raise ValidationError("Last name is required.")
        
        if len(last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters long.")
        
        return last_name
    
    def clean(self):
        """Overall form validation."""
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        # Ensure payment method is selected
        if not payment_method:
            raise ValidationError("Please select a payment method.")
        
        return cleaned_data

