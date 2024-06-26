from django.urls import path
from products import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'
urlpatterns = [
    path("", views.list_view, name="list"),
    path("create/", views.create_view, name="create"),
    path("<int:product_id>/", views.detail_view, name="detail"),
    path("<int:product_id>/update/", views.update_view, name="update"),
    path("<int:product_id>/delete/", views.delete_view, name="delete"),
    path("<int:product_id>/like/", views.like_view, name='like'),
    path("search/", views.search_view, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)