from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    search_fields = ('name', 'contact_person')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'supplier', 'price', 'stock_quantity', 'reorder_level')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'sku')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'movement_type', 'timestamp')
    list_filter = ('movement_type', 'timestamp')
    search_fields = ('product__name', 'notes')