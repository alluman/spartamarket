from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    hashtags = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'image']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, author):
        product_instance = super().save(commit=False)
        product_instance.author = author
        product_instance.save()
        return product_instance