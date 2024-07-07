from django import forms
from .models import Product, StockMovement, CustomUser
from django.contrib.auth.forms import UserCreationForm

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

class ProductForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'sku', 'category', 'supplier', 'price', 'stock_quantity', 'reorder_level']

class StockMovementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'movement_type', 'notes']

class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})