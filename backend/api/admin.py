"""Admin configuration for the API app."""

from django.contrib import admin

from .models import (
    Cart,
    CartItem,
    Category,
    EbikeSpec,
    Order,
    OrderItem,
    Product,
    ProductVariant,
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(EbikeSpec)
admin.site.register(ProductVariant)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)