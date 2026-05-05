from django.db import models
from django.urls import reverse
from pytils.translit import slugify

from core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})


class SubCategory(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='subcategories', verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.category.name} → {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products', verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products', verbose_name='Подкатегория'
    )
    name = models.CharField(max_length=300, verbose_name='Название')
    slug = models.SlugField(max_length=300, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True, verbose_name='Цена (UZS)'
    )
    price_old = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True, verbose_name='Старая цена'
    )
    min_order = models.PositiveIntegerField(default=1, verbose_name='Мин. заказ')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_featured = models.BooleanField(default=False, verbose_name='Актуальное')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        if self.price_old and self.price and self.price_old > self.price:
            return int((1 - self.price / self.price_old) * 100)
        return None


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images', verbose_name='Товар'
    )
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['order']

    def __str__(self):
        return f'Фото: {self.product.name}'
