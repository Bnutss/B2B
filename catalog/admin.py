from django.contrib import admin
from django.utils.html import format_html
from .models import Category, SubCategory, Product, ProductImage


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0
    fields = ['name', 'slug', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_main', 'order', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" style="border-radius:4px"/>', obj.image.url)
        return '—'

    preview.short_description = 'Превью'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'preview']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="40" style="border-radius:4px"/>', obj.image.url)
        return '—'

    preview.short_description = 'Фото'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'subcategory',
        'price', 'price_old', 'is_active',
        'is_featured', 'in_stock', 'order'
    ]
    list_editable = ['price', 'is_active', 'is_featured', 'in_stock', 'order']
    list_filter = ['category', 'subcategory', 'is_active', 'is_featured', 'in_stock']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    fieldsets = (
        ('Основное', {
            'fields': ('category', 'subcategory', 'name', 'slug', 'description')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'price_old', 'min_order', 'in_stock')
        }),
        ('Настройки', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
    )
