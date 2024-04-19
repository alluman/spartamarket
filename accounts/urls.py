from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

app_name='accounts'
urlpatterns=[
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update/<str:username>/', views.userupdate_view, name="userupdate"),
    path('<int:user_id>/follow/', views.follow_view, name='follow'),
    path('delete/', views.delete_view, name='delete'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)