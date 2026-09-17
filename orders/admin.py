from django.contrib import admin

from .models import Category, Order, OrderItem, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'is_active',
        'order',
    )
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_available',
        'is_featured',
    )
    list_filter = (
        'category',
        'is_available',
        'is_featured',
    )
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product',
        'rating',
        'created_at',
    )
    list_filter = ('rating',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'total_price',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'full_name',
        'phone',
        'email',
    )
    inlines = [OrderItemInline]