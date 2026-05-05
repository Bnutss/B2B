from django.shortcuts import render
from catalog.models import Product, Category
from banners.models import Banner


def home(request):
    featured = Product.objects.filter(is_active=True, is_featured=True)[:16]
    categories = Category.objects.filter(is_active=True)
    banners = Banner.objects.filter(is_active=True).order_by('order')

    context = {
        'featured': featured,
        'categories': categories,
        'banners': banners,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')
