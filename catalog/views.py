from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product


def search_autocomplete(request):
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        products = Product.objects.filter(
            is_active=True, name__icontains=q
        ).select_related('category').prefetch_related('images')[:8]
        for p in products:
            img = p.images.first()
            results.append({
                'name': p.name,
                'slug': p.slug,
                'price': str(int(p.price)) if p.price else None,
                'category': p.category.name,
                'image': img.image.url if img else None,
                'url': p.get_absolute_url(),
            })
    return JsonResponse({'results': results})


def catalog_list(request):
    categories = Category.objects.filter(is_active=True).prefetch_related('subcategories')
    products = Product.objects.filter(is_active=True).select_related('category')

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(name__icontains=q)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
    }
    return render(request, 'catalog/list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(
        category=category, is_active=True
    ).select_related('category', 'subcategory')

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:6]

    context = {
        'product': product,
        'images': images,
        'related': related,
    }
    return render(request, 'catalog/product.html', context)
