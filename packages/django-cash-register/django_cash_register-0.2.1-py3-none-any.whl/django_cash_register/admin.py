from django.contrib import admin
from .models import Category, Product, ProductHistory, CartList, Cart,  ActionType, Unit, Currency


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Categories for products"""

    fields = ['name']

    list_display = fields


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Units for products"""

    fields = ['name']

    list_display = fields


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    """History"""

    fields = ['product', 'action_date', 'action', 'name', 'image', 'barcode', 'qrcode', 'category', 'product_count',
              'unit', 'weight', 'purchase_price', 'price', 'promotion_price', 'promotion_product', 'active', 'exists']

    readonly_fields = fields
    search_fields = ['action_date', 'name', 'image', 'barcode', 'qrcode', 'category__name', 'product_count',
                     'purchase_price', 'price', 'unit__name', 'weight', 'promotion_price', 'promotion_product',
                     'active', 'exists']
    list_display = fields
    list_display_links = fields[:3]
    list_filter = ['category', 'action_date', 'action', 'promotion_product', 'unit', 'active', 'exists']
    change_form_ = 'admin/django_cash_register/change_form_object_tools.html'

    @classmethod
    def has_add_permission(cls, request):
        """Remove add and save and add another button"""

        return False

    @classmethod
    def has_change_permission(cls, request, obj=None):
        """Remove change button"""

        return False

    def change_view(self, request, object_id, extra_context=None, **kwargs):
        """Customize add/edit form"""

        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        return super(ProductHistoryAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def get_actions(self, request):
        actions = super(ProductHistoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Products."""

    fields = ['name', 'image', 'barcode', 'qrcode', 'category', 'product_count', 'weight', 'unit', 'purchase_price',
              'price', 'promotion_price', 'promotion_product', 'active']

    list_display = fields
    list_filter = ['category', 'promotion_product', 'unit', 'active']
    search_fields = ['name', 'image', 'barcode', 'qrcode', 'category__name', 'product_count', 'unit__name', 'weight',
                     'purchase_price', 'price', 'promotion_price', 'promotion_product', 'active']


@admin.register(CartList)
class CartListAdmin(admin.ModelAdmin):
    """Carts."""
    fields = ['user', 'last_update']
    list_display = fields
    readonly_fields = ['last_update']
    list_filter = fields


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Open carts"""

    fields = ['cart_number', 'product', 'product_count']

    list_display = fields
    list_filter = ['cart_number']
    search_fields = fields[1:]


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    """Action types."""

    fields = ['name']

    list_display = fields

    @classmethod
    def has_add_permission(cls, request):
        """Remove add and save and add another button"""

        return False

    @classmethod
    def has_change_permission(cls, request, obj=None):
        """Remove change button"""

        return False

    def change_view(self, request, object_id, extra_context=None, **kwargs):
        """Customize add/edit form"""

        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        return super(ActionTypeAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def get_actions(self, request):
        actions = super(ActionTypeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Currencies"""

    fields = ['value', 'float_right', 'active']

    list_display = fields
