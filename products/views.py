from django.shortcuts import render, redirect
from products.models import Product
from products.forms import ProductForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST


# Create your views here.
def list_view(request):
    products = Product.objects.all()
    return render(request, "products/list.html", {"products":products})

@login_required
def create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request=request) 
        if form.is_valid():
            form.save(author=request.user)  
            return redirect('products:list')  
    else:
        form = ProductForm(request=request) 
    return render(request, 'products/create.html', {"form": form})

def detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required
def update_view(request, product_id):
    form = ProductForm(request=request)
    product = get_object_or_404(Product, pk=product_id)
    if product.author != request.user:
        messages.warning(request, message='허가되지 않은 접근입니다')
        return redirect("products:detail", product_id)
    form = ProductForm(request.POST or None, instance=product, request=request)
    if request.method == 'POST':
        if form.is_valid():
            form.save(author=request.user)  
            return redirect('products:list')
    return render(request, 'products/create.html', {"form":form})

@login_required
def delete_view(request, product_id):
    form = ProductForm(request=request)
    product = get_object_or_404(Product, pk=product_id)
    if product.author != request.user:
        messages.warning(request, message='허가되지 않은 접근입니다')
        return redirect("products:detail", product_id)
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return redirect('products:list')

@require_POST
def like_view(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        if product.like_user.filter(pk=request.user.pk).exists():
            product.like_user.remove(request.user)
        else:
            product.like_user.add(request.user)
        referer_url = request.META.get('HTTP_REFERER')
        return redirect(referer_url or 'products:list')
    return redirect('accounts:login')