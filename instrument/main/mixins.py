from django.urls import reverse, reverse_lazy

from .forms import CategoryForm, CommentForm, ProductForm, ProductTypeForm
from .models import Category, Comment, Product, ProductType, User


class ProductCreateUpdateDeleteMixin:
    """Миксин для создания/редактирования/удаления продукта."""

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('main:creates')
    pk_url_kwarg = 'product_id'


class CategoryCreateUpdateDeleteMixin:
    """Миксин для создания/редактирования/удаления категории."""

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('main:creates')
    slug_url_kwarg = 'category'


class ProductTypeCreateUpdateDeleteMixin:
    """Миксин для создания/редактирования/удаления типа категории."""

    model = ProductType
    form_class = ProductTypeForm
    slug_url_kwarg = 'product_type'
    success_url = reverse_lazy('main:creates')


class CommentMixinCreateUpdateDeleteMixin:
    """Миксин для создания/редактирования/удаления комментария."""

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'main:product_detail',
            kwargs={
                'category': self.kwargs['category'],
                'product_type': self.kwargs['product_type'],
                'product_id': self.kwargs['product_id']
            }
        )


class DispatchMixin:
    """
    Миксин для перенаправления нежелательного
    пользователя на другую страницу
    """

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            return reverse(
                'main:product_detail',
                kwargs={
                    'category': self.kwargs['category'],
                    'product_type': self.kwargs['product_type'],
                    'product_id': self.kwargs['product_id']
                }
            )
        return super().dispatch(request, *args, **kwargs)


class CartAndFavViewMixin:
    """Миксин для просмотра содержимого корзины и избранного."""

    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
