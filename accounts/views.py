from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

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
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, "사용 중인 email입니다.")
                return render(request, 'accounts/signup.html', {"form":form})
            user = form.save()
            login(request, user)
            return redirect('products:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {"form":form})

@login_required
def userupdate_view(request, username):
    user = get_object_or_404(User, username=username)
    referer_url = request.META.get('HTTP_REFERER')
    if user != request.user:
        messages.warning(request, message='권한이 없습니다.')
        return redirect(referer_url or 'products:list')
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        context = {
            'user_form':user_form,
            'password_form':password_form
        }
        if user_form.is_valid() and password_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if email != user.email and User.objects.filter(email=email).exists():
                messages.error(request, "사용 중인 email입니다.")
                return render(request, 'accounts/user_update.html', context)
            old_password = password_form.cleaned_data.get('old_password')
            new_password1 = password_form.cleaned_data.get('new_password1')
            if old_password == new_password1:
                messages.error(request, '새 비밀번호는 기존 비밀번호와 달라야 합니다.')
                return render(request, 'accounts/user_update.html', context)
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, '비밀번호가 변경되었습니다.')
            return redirect('products:list')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
        context = {
            'user_form': user_form,
            'password_form': password_form
        }
    return render(request, 'accounts/user_update.html', context)

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

@login_required
def delete_view(request):
    if request.method == 'POST':
        Product.objects.filter(author=request.user).delete()
        Product.objects.filter(like_user=request.user).delete()
        User.objects.filter(followers=request.user).delete()
        User.objects.filter(following=request.user).delete()
        request.user.delete()
        logout(request)
        messages.success(request, '계정이 성공적으로 삭제되었습니다.')
        return redirect('products:list')