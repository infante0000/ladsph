from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'slug', 'in_stock')
    list_editable = ('price', 'in_stock')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'product', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer', 'date_ordered', 'complete')


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer',  'shipping_date', 'city', 'order')


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Category, CategoryAdmin)
