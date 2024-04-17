from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField()
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    like_user = models.ManyToManyField('accounts.User', related_name='like_products', )