from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='list'),
    path('search/', views.search_autocomplete, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product'),
]
