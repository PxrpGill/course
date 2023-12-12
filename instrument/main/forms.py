from django import forms

from .models import Category, Comment, Product, ProductType


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
