from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from accounts.forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib.auth.decorators import login_required
from products.models import Product
# Create your views here.
def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products:list')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('products:list')

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {"form":form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    products = Product.objects.filter(author=user.id)
    like_products = Product.objects.filter(like_user=user.id)
    context = {
        'user': user,
        'products': products,
        'like_products':like_products
    }
    return render(request, 'accounts/profile.html', context)

def follow_view(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("accounts:profile", username=member.username)
    return redirect("accounts:login")