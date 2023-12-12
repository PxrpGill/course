from django.contrib import admin

from .models import Cart, Category, Comment, Favorite, Product, ProductType

# admin 1234


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'product_type',
        'is_published',
        'pub_date',
        'created_at'
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_display_links = ('title',)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_display_links = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'created_at',
        'product_id'
    )
    search_fields = ('author',)
    list_display_links = ('author',)
    list_filter = ('created_at',)


class CartAndFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    list_filter = ('product',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cart, CartAndFavoriteAdmin)
admin.site.register(Favorite, CartAndFavoriteAdmin)
