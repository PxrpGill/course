import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import (
    Product, Comment, Category, ProductType, User, Cart
)
from .forms import ProductForm, CommentForm, CategoryForm, ProductTypeForm


paginate = 8
paginate_category = 16
paginate_create = 6


class MainPageListView(ListView):
    """Отображение главной страницы."""

    model = Product
    context_object_name = 'product'
    paginate_by = paginate
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


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание продукта."""

    model = Product
    form_class = ProductForm
    permission_required = 'main.add_product'
    template_name = 'main/product/create_product.html'
    success_url = reverse_lazy('main:creates')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование содержимого продукта."""

    model = Product
    form_class = ProductForm
    permission_required = 'main.change_product'
    template_name = 'main/product/update_product.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse(
            'main:product_detail',
            kwargs={
                'category': self.kwargs['category'],
                'product_type': self.kwargs['product_type'],
                'product_id': self.get_object().pk
            }
        )


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление продукта."""

    model = Product
    form_class = ProductForm
    permission_required = 'main.delete_product'
    pk_url_kwarg = 'product_id'
    template_name = 'main/product/delete_product.html'

    def get_success_url(self):
        return reverse(
            'main:creates'
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.delete()
        return HttpResponseRedirect(success_url)


class CategoryListView(ListView):
    """Отображение списка категорий."""

    model = Category
    template_name = 'main/category/category_list.html'
    paginate_by = paginate_category

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


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание категории."""

    model = Category
    form_class = CategoryForm
    permission_required = 'main.add_category'
    template_name = 'main/category/category_create.html'
    success_url = reverse_lazy('main:creates')


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование категории."""

    model = Category
    form_class = CategoryForm
    permission_required = 'main.change_category'
    slug_url_kwarg = 'category'
    template_name = 'main/category/category_update.html'
    success_url = reverse_lazy('main:creates')


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление категории."""

    model = Category
    form_class = CategoryForm
    permission_required = 'main.delete_category'
    slug_url_kwarg = 'category'
    template_name = 'main/category/category_delete.html'

    def get_success_url(self):
        return reverse(
            'main:creates'
        )

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
    paginate_by = paginate
    slug_url_kwarg = 'product_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            product_type=self.object
        )
        return context


class ProductTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование типа продукта."""

    model = ProductType
    form_class = ProductTypeForm
    permission_required = 'main.change_producttype'
    slug_url_kwarg = 'product_type'
    template_name = 'main/product_type/product_type_update.html'
    success_url = reverse_lazy('main:creates')


class ProductTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление типа продукта."""

    model = ProductType
    form_class = ProductTypeForm
    permission_required = 'main.delete_producttype'
    slug_url_kwarg = 'product_type'
    template_name = 'main/product_type/product_type_delete.html'

    def get_success_url(self):
        return reverse(
            'main:creates'
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.delete()
        return HttpResponseRedirect(success_url)


class ProductTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание типа продукта."""

    model = ProductType
    form_class = ProductTypeForm
    permission_required = 'main.add_producttype'
    template_name = 'main/product_type/product_type_create.html'
    success_url = reverse_lazy('main:creates')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'main/comment/update_comment.html'
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


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'main/comment/delete_comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'main:product_detail',
            kwargs={
                'category': self.kwargs['category'],
                'product_type': self.kwargs['product_type'],
                'product_id': self.kwargs['product_id']
            }
        )

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

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.delete()
        return HttpResponseRedirect(success_url)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'main/product/detail_product.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product_id = get_object_or_404(
            Product,
            pk=self.kwargs['product_id']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'main:product_detail',
            kwargs={
                'category': self.kwargs['category'],
                'product_type': self.kwargs['product_type'],
                'product_id': self.kwargs['product_id']
            }
        )


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
    paginate_by = paginate_create

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
