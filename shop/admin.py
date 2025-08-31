# admin.py

from django.contrib import admin
from .models import Product, CartItem, Suggestion, Profile, Order, OrderItem,Coupon

admin.site.register(Product)
admin.site.register(Coupon)
admin.site.register(Suggestion)
admin.site.register(Profile)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'subtotal', 'added_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal_display',)
    fields = ('product', 'quantity', 'subtotal_display')

    def subtotal_display(self, obj):
        if obj.pk and obj.product and obj.product.price is not None:
            return obj.subtotal()
        return "-"
    subtotal_display.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status')
    inlines = [OrderItemInline]


# ✅ New: Show subtotal in OrderItem list view
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'subtotal_display')

    def subtotal_display(self, obj):
        if obj.product and obj.product.price is not None:
            return obj.subtotal()
        return "-"
    subtotal_display.short_description = 'Subtotal'
