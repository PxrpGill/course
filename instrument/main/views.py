import datetime

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)
from django.urls import reverse_lazy

from .forms import CommentForm, CustomUserChangeForm, RatingForm, ProductFilterForm
from .mixins import (
    CategoryCreateUpdateDeleteMixin,
    CommentMixinCreateUpdateDeleteMixin,
    DispatchMixin,
    ProductCreateUpdateDeleteMixin,
    ProductTypeCreateUpdateDeleteMixin,
    CartAndFavViewMixin
)
from .models import (
    Cart,
    Category,
    Comment,
    Product,
    ProductType,
    User,
    Favorite,
    ProductRating,
    OrderHistory
)


PAGINATE = 9
PAGINATE_CATEGORY = 15
PAGINATE_CREATE = 6


class MainPageListView(ListView):
    """Отображение главной страницы."""

    model = Product
    paginate_by = PAGINATE
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_published=True)
        context['favorites'] = Favorite.objects.get(user=self.request.user)
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
        context['favorites'] = Favorite.objects.get(user=self.request.user)
        context['form'] = CommentForm()
        context['star_form'] = RatingForm()
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
    context_object_name = 'select_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.filter(
            category=self.get_object()
        )
        context['favorites'] = Favorite.objects.get(user=self.request.user)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.filter(category=self.object)
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
    context_object_name = 'product_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_published=True)
        context['favorites'] = Favorite.objects.get(user=self.request.user)

        form = ProductFilterForm(self.request.GET)
        products = Product.objects.filter(
            product_type=self.object
        )

        if form.is_valid():
            max_price = form.cleaned_data['max_price']
            manufacturer = form.cleaned_data['manufacturer']

            if max_price:
                products = products.filter(price__lte=max_price)
            if manufacturer:
                products = products.filter(manufacturer=manufacturer)

        context['form'] = form
        context['products'] = products

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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    form_class = CustomUserChangeForm
    template_name = 'main/change_profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'main:profile_detail',
            kwargs={
                'username': self.kwargs['username']
            }
        )

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.username != request.user.username:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)


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


class CartDetailView(
    LoginRequiredMixin,
    CartAndFavViewMixin,
    DetailView
):
    """Отображение содержимого корзины."""

    template_name = 'main/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        context['cart_price'] = sum([product.price for product in cart.product.all()])
        return context


class CartDeleteItemView(LoginRequiredMixin, DeleteView):
    """Удаление продукта из корзины."""

    def post(self, request, product_id):
        user = request.user
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=user)
        cart.product.remove(product)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'main:cart_view',
            kwargs={
                'username': self.request.user.username
            }
        )


class FavoriteCreateView(LoginRequiredMixin, View):
    """Добавление продукта в избранное."""

    def post(self, request, product_id):
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_id)
        favorite.product.add(product)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FavoriteDetailView(
    LoginRequiredMixin,
    CartAndFavViewMixin,
    DetailView
):
    """Отображение содержимого избранного."""

    template_name = 'main/favorite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorite, create = Favorite.objects.get_or_create(user=self.request.user)
        context['favorites'] = Favorite.objects.get(user=self.request.user)
        context['favorite'] = favorite
        return context


class FavoriteDeleteItemView(LoginRequiredMixin, DeleteView):
    """Удаление продукта из избранного."""

    def post(self, request, product_id):
        user = request.user
        product = Product.objects.get(id=product_id)
        favorite = Favorite.objects.get(user=user)
        favorite.product.remove(product)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        return reverse_lazy(
            'main:favorite_view',
            kwargs={
                'username': self.request.user.username
            }
        )


class SearchResultsListView(ListView):
    """Система поиска продуктов на сайте."""

    model = Product
    context_object_name = 'products'
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_published=True)
        context['favorites'] = Favorite.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        query = query.title()
        object_list = Product.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


class AddToOrderHistory(LoginRequiredMixin, CreateView):
    """Добавление заказа в историю."""

    slug_url_kwarg = 'username'
    slug_field = 'username'

    def post(self, request, username):
        user = User.objects.get(username=username)
        cart = get_object_or_404(Cart, user=user)
        products = cart.product.all()
        order = OrderHistory.objects.create(user=user, cart=cart)
        order.product.set(products)
        cart.product.clear()
        return redirect('main:cart_view', username)

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs['username'])
        instance = Cart.objects.get(user=user)

        if instance.user != request.user:
            return reverse(
                'main:cart_view',
                kwargs={
                    'username': user
                }
            )
        return super().dispatch(request, *args, **kwargs)


class OrderHistoryListView(ListView):
    model = OrderHistory
    template_name = 'main/order.html'

    def get_queryset(self):
        return OrderHistory.objects.filter(user=self.request.user)
