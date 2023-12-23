from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Published(models.Model):
    """Класс-родитель с полями is_published, created_at."""

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
        abstract = True


class Manufacturer(Published):
    """Таблица в БД - Производитель."""

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название производителя'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'Производители'
        ordering = ('-created_at',)


class Category(Published):
    """Таблица в БД - Категория."""

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

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class ProductType(Published):
    """Таблица в БД - Тип продукта."""

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

    class Meta:
        verbose_name = 'тип продукта'
        verbose_name_plural = 'Типы продуктов'

    def __str__(self):
        return self.title


class Product(Published):
    """Таблица в БД - Продукт."""

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
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Производетель'
    )

    class Meta:
        verbose_name = 'инструмент'
        verbose_name_plural = 'Инструменты'
        ordering = ('pub_date',)

    def __str__(self):
        return self.title


class Comment(Published):
    """Таблица в БД - Комментарий."""

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


    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.author


class CartAndFavModel(models.Model):
    """Класс-родитель с полями user, product."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ManyToManyField(
        Product,
        verbose_name='Продукт',
    )

    class Meta:
        abstract = True


class Cart(CartAndFavModel):
    """Таблица в БД - Корзина."""

    def __str__(self):
        return f'{self.user} добавил в корзину {self.product}'

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'


class OrderHistory(models.Model):
    """Запись в БД - История заказов."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='Обрабатываемая корзина'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ManyToManyField(
        Product,
        verbose_name='Продукт'
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время создания'
    )

    def __str__(self):
        return f'{self.user} - {self.cart}'

    class Meta:
        verbose_name = 'история заказов'
        verbose_name_plural = 'Истории заказов'
        ordering = ('-created_at',)


class Favorite(CartAndFavModel):
    """Таблица в БД - Избранное."""

    def __str__(self):
        return f'{self.user} добавил в избранное {self.product}'

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'


class Rating(models.Model):
    """Рейтинг продукта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5')
        ],
        verbose_name='Рейтинг'
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Добавлено'
    )

    def __str__(self):
        return f'{self.user} - {self.product} - {self.rating}'

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ('-created_at',)

