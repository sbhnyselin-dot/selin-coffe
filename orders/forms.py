from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name',
            'phone',
            'email',
            'address',
            'note',
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your full name',
                    'class': 'form-control',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Phone number',
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email address',
                    'class': 'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Delivery address',
                    'class': 'form-control',
                }
            ),
            'note': forms.Textarea(
                attrs={
                    'placeholder': 'Any special request?',
                    'class': 'form-control',
                    'rows': 4,
                }
            ),
        }