from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'author', 'display_like_users')

    def display_like_users(self, obj):
        return ", ".join([user.username for user in obj.like_user.all()])
    display_like_users.short_description = 'Liked by'

admin.site.register(Product, ProductAdmin)