# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('products'))

    def product_count(self, obj):
        return obj.product_count
    product_count.short_description = "Products"
    product_count.admin_order_field = 'product_count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'thumbnail_preview',
        'name',
        'category',
        'price',
        'stock',
        'is_active',
        'click_count',
        'trending_badge',
        'created_at',
    )
    list_filter = ('is_active', 'category', 'created_at', 'price')
    search_fields = ('name', 'description', 'slug', 'category__name')
    readonly_fields = ('id', 'slug', 'click_count', 'created_at', 'updated_at', 'thumbnail_preview')
    autocomplete_fields = ('category',)
    prepopulated_fields = {}
    ordering = ('-created_at',)
    list_per_page = 50

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'price', 'stock', 'is_active')
        }),
        ('Media', {
            'fields': ('thumbnail', 'thumbnail_preview', 'file'),
            'description': 'Preview updates automatically after saving.'
        }),
        ('Stats & Timestamps', {
            'fields': ('click_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;object-fit:cover;">', obj.thumbnail.url)
        return "(No image)"
    thumbnail_preview.short_description = "Preview"

    def name_with_slug(self, obj):
        return format_html("{}\n<br><small style='color:#666'>{}</small>", obj.name, obj.slug)
    name_with_slug.short_description = "Product"
    name_with_slug.admin_order_field = 'name'

    def trending_badge(self, obj):
        if obj.click_count > 100:
            return format_html('<span style="background:#00d26a;color:white;padding:3px 8px;border-radius:4px;font-size:11px;">TRENDING</span>')
        return "—"
    trending_badge.short_description = "Status"

    def get_list_display(self, request):
        display = list(self.list_display)
        if 'name' in display:
            display[display.index('name')] = 'name_with_slug'
        return display

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return fields + ('is_active',)
        return fields