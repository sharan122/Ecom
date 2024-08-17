from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description','camera', 
            'display_type', 'display_size', 'processor', 'battery', 
            'os', 'network_type','brand'
        ]
