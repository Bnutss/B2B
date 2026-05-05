from django.db import models
from core.models import TimeStampedModel


class Banner(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name='Заголовок', blank=True)
    image = models.ImageField(upload_to='banners/', verbose_name='Изображение')
    link = models.URLField(blank=True, verbose_name='Ссылка')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order']

    def __str__(self):
        return self.title or f'Баннер #{self.pk}'
