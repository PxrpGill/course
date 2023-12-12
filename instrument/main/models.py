from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL;'
                  ' разрешены символы латиницы, цифры,'
                  ' дефис и подчёркивание.'
    )
    image = models.ImageField(
        upload_to='category/',
        null=True,
        blank=True,
        verbose_name='Фото категории'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class ProductType(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name='Название типа продукта'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL;'
                  ' разрешены символы латиницы, цифры,'
                  ' дефис и подчёркивание.'
    )
    # ManyToOne
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='types'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'тип продукта'
        verbose_name_plural = 'Типы продуктов'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name='Название инструмента'
    )
    description = models.TextField(
        verbose_name='Описание инструмента'
    )
    parameters = models.TextField(
        verbose_name='Параметры инструмента'
    )
    # OneToMany
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products_category'
    )
    # OneToMany
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        verbose_name='Тип продукта',
        related_name='products_type'
    )
    image = models.ImageField(
        upload_to='product/',
        null=True,
        blank=True,
        verbose_name='Фото инструмента'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.'
    )
    price = models.FloatField(
        verbose_name='Цена',
        validators=[MinValueValidator(0)],
        help_text='Цена не может быть ниже нуля.',
        default=1
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'инструмент'
        verbose_name_plural = 'Инструменты'
        ordering = ('pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='ID продукта',
        related_name='comments'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.author


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ManyToManyField(
        Product,
        verbose_name='Продукт'
    )

    def __str__(self):
        return f'{self.user} добавил в корзину {self.product}'

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'


class Favorite(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )

    def __str__(self):
        return f'{self.user} добавил в избранное {self.product}'

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
