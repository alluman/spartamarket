from django.shortcuts import render, redirect
from products.models import Hashtag, Product
from products.forms import ProductForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
import re

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
        if form.is_valid():
            content = form.cleaned_data.get('content', '')
            hashtags = form.cleaned_data.get('hashtags', '')
            #본문이랑 해시태그에서 해시태그 가져오는 코드
            tags = [tag.strip()[1:] for tag in (content + ' ' + hashtags).strip().split() if tag.strip() != '' and tag.strip()[0] == '#']
            valid_tag = re.compile(r'^[가-힣A-Za-z0-9]+$')
            for tag_name in tags:
                if not valid_tag.match(tag_name):
                    messages.error(request, '해시태그는 한글, 영어, 숫자만 포함할 수 있습니다: ' + tag_name)
                    return render(request, 'products/create.html', {"form": form})
            product = form.save(author=request.user)
            for tag_name in tags:
                tag, _ = Hashtag.objects.get_or_create(name=tag_name)
                product.hashtags.add(tag)           
            return redirect('products:list')
    else:
        form = ProductForm(request=request) 
    return render(request, 'products/create.html', {"form":form})

def detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.view += 1
    product.save()
    return render(request, 'products/detail.html', {'product':product})

@login_required
def update_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.author != request.user:
        messages.warning(request, message='권한이 없습니다.')
        return redirect("products:detail", product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, request=request)
        if form.is_valid():
            product.hashtags.clear()
            content = form.cleaned_data.get('content', '')
            hashtags = form.cleaned_data.get('hashtags', '')
            #본문이랑 해시태그에서 해시태그 가져오는 코드
            tags = [tag.strip()[1:] for tag in (content + ' ' + hashtags).strip().split() if tag.strip() != '' and tag.strip()[0] == '#']
            valid_tag = re.compile(r'^[가-힣A-Za-z0-9]+$')
            for tag_name in tags:
                if not valid_tag.match(tag_name):
                    messages.error(request, '해시태그는 한글, 영어, 숫자만 포함할 수 있습니다: ' + tag_name)
                    return render(request, 'products/product_update.html', {"form": form})
            product = form.save(author=request.user)
            for tag_name in tags:
                tag, _ = Hashtag.objects.get_or_create(name=tag_name)
                product.hashtags.add(tag)           
            return redirect('products:list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_update.html', {"form":form})
        
@login_required
def delete_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.author != request.user:
        messages.warning(request, message='권한이 없습니다.')
        return redirect("products:detail", product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, '삭제되었습니다.')
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