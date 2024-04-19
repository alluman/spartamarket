from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    hashtags = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'image']
        