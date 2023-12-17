from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Category, Comment, Product, ProductType, User


class ProductForm(forms.ModelForm):
    """Форма для создания продукта."""

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Форма для комментария."""

    class Meta:
        model = Comment
        fields = ('text',)


class CategoryForm(forms.ModelForm):
    """Форма для категорий."""

    class Meta:
        model = Category
        fields = '__all__'


class ProductTypeForm(forms.ModelForm):
    """Форма для типа продукта."""

    class Meta:
        model = ProductType
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
