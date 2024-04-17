from django.shortcuts import render, redirect
from products.models import Hashtag, Product
from products.forms import ProductForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Q

# Create your views here.
def list_view(request):
    sort = request.GET.get('sort', '-created_at')
    if sort == "-like_user":
        order_fields = ['-likes_count', '-created_at']
        products = Product.objects.annotate(likes_count=Count('like_user')).order_by(*order_fields)
    else:
        products = Product.objects.all().order_by(sort)
    return render(request, "products/list.html", {"products":products})

@login_required
def create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, request=request) 
        print(ProductForm)
        if form.is_valid():
            product = form.save(author=request.user)
            content = form.cleaned_data.get('content', '')
            hashtags = form.cleaned_data.get('hashtags', '')
            tags = [tag.strip()[1:] for tag in (content + ' ' + hashtags).strip().split() if tag.strip() != '' and tag.strip()[0] == '#']
            for tag_name in tags:
                tag, created = Hashtag.objects.get_or_create(name=tag_name)
                product.hashtags.add(tag)                   
            return redirect('products:list') 
    else:
        form = ProductForm(request=request) 
    return render(request, 'products/create.html', {"form": form})

def detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.view = product.view +1
    product.save()
    return render(request, 'products/detail.html', {'product':product})

@login_required
def update_view(request, product_id):
    form = ProductForm(request=request)
    product = get_object_or_404(Product, pk=product_id)
    if product.author != request.user:
        messages.warning(request, message='권한이 없습니다.')
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
        messages.warning(request, message='권한이 없습니다.')
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

def search_view(request):
    keyword = request.GET.get('keyword', '')
    search_products = Product.objects.filter(
        Q(title__icontains=keyword) |
        Q(content__icontains=keyword) |
        Q(author__username__icontains=keyword)|
        Q(hashtags__name__icontains=keyword)
    )
    context= {
        'keyword':keyword,
        'search_products': set(search_products)
    }
    return render(request, 'products/search.html', context)