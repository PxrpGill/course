import datetime

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, View
)

from .forms import CommentForm
from .models import Cart, Category, Comment, Product, ProductType, User
from .mixins import (
    ProductCreateUpdateDeleteMixin,
    CategoryCreateUpdateDeleteMixin,
    ProductTypeCreateUpdateDeleteMixin,
    CommentMixinCreateUpdateDeleteMixin,
    DispatchMixin
)

PAGINATE = 8
PAGINATE_CATEGORY = 16
PAGINATE_CREATE = 6


class MainPageListView(ListView):
    """Отображение главной страницы."""

    model = Product
    context_object_name = 'product'
    paginate_by = PAGINATE
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_published=True)
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_published=True,
            pub_date__lte=datetime.datetime.now()
        )
        return queryset


class ProductDetailView(DetailView):
    """Детальное отображение продукта"""

    model = Product
    template_name = 'main/product/detail_product.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            product_id=self.kwargs['product_id']
        )
        context['form'] = CommentForm()
        return context


class ProductCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ProductCreateUpdateDeleteMixin,
    CreateView
):
    """Создание продукта."""

    permission_required = 'main.add_product'
    template_name = 'main/product/create_product.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ProductCreateUpdateDeleteMixin,
    UpdateView
):
    """Редактирование содержимого продукта."""

    permission_required = 'main.change_product'
    template_name = 'main/product/update_product.html'


class ProductDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ProductCreateUpdateDeleteMixin,
    DeleteView
):
    """Удаление продукта."""

    permission_required = 'main.delete_product'
    template_name = 'main/product/delete_product.html'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.delete()
        return HttpResponseRedirect(success_url)


class CategoryListView(ListView):
    """Отображение списка категорий."""

    model = Category
    template_name = 'main/category/category_list.html'
    paginate_by = PAGINATE_CATEGORY

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_published=True
        )
        return queryset


class CategoryDetailView(DetailView):
    """Детальное отображение категории."""

    model = Category
    template_name = 'main/category/category_detail.html'
    slug_url_kwarg = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.filter(
            category=self.get_object()
        )
        return context


class CategoryCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CategoryCreateUpdateDeleteMixin,
    CreateView
):
    """Создание категории."""

    permission_required = 'main.add_category'
    template_name = 'main/category/category_create.html'


class CategoryUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CategoryCreateUpdateDeleteMixin,
    UpdateView
):
    """Редактирование категории."""

    permission_required = 'main.change_category'
    template_name = 'main/category/category_update.html'


class CategoryDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CategoryCreateUpdateDeleteMixin,
    DeleteView
):
    """Удаление категории."""

    permission_required = 'main.delete_category'
    template_name = 'main/category/category_delete.html'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.image.delete()
        instance.delete()
        return HttpResponseRedirect(success_url)


class ProductTypeDetailView(DetailView):
    """Детальное отображение."""

    model = ProductType
    template_name = 'main/product_type/product_type_detail.html'
    paginate_by = PAGINATE
    slug_url_kwarg = 'product_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            product_type=self.object
        )
        return context


class ProductTypeUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ProductTypeCreateUpdateDeleteMixin,
    UpdateView
):
    """Редактирование типа продукта."""

    permission_required = 'main.change_producttype'
    template_name = 'main/product_type/product_type_update.html'


class ProductTypeDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ProductTypeCreateUpdateDeleteMixin,
    DeleteView
):
    """Удаление типа продукта."""

    permission_required = 'main.delete_producttype'
    template_name = 'main/product_type/product_type_delete.html'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.delete()
        return HttpResponseRedirect(success_url)


class ProductTypeCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ProductTypeCreateUpdateDeleteMixin,
    CreateView
):
    """Создание типа продукта."""

    permission_required = 'main.add_producttype'
    template_name = 'main/product_type/product_type_create.html'


class CommentUpdateView(
    LoginRequiredMixin,
    CommentMixinCreateUpdateDeleteMixin,
    DispatchMixin,
    UpdateView
):
    """Редактирование комментария."""

    template_name = 'main/comment/update_comment.html'


class CommentDeleteView(
    LoginRequiredMixin,
    CommentMixinCreateUpdateDeleteMixin,
    DispatchMixin,
    DeleteView
):
    """Удаление комментария."""

    template_name = 'main/comment/delete_comment.html'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.delete()
        return HttpResponseRedirect(success_url)


class CommentCreateView(
    LoginRequiredMixin,
    CommentMixinCreateUpdateDeleteMixin,
    CreateView
):
    """Создание комментария."""

    template_name = 'main/product/detail_product.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product_id = get_object_or_404(
            Product,
            pk=self.kwargs['product_id']
        )
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DeleteView):
    """Отображение профиля."""

    model = User
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'main/profile.html'


class CreatesListView(ListView):
    """Страница для наполнителя."""

    model = Product
    context_object_name = 'products'
    template_name = 'creates.html'
    paginate_by = PAGINATE_CREATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.all()
        context['categories'] = Category.objects.all()
        return context


class CartCreateView(LoginRequiredMixin, View):
    """Добавление продукта в корзину."""

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_id)
        cart.product.add(product)
        return redirect('main:index')


class CartDetailView(LoginRequiredMixin, DetailView):
    """Отображение содержимого корзины."""

    model = Cart
    template_name = 'main/cart.html'
