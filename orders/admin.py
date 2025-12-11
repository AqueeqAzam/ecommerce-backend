# orders/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number_link',
        'full_name',
        'mobile',
        'total_amount_colored',
        'paid_amount',
        'status_badge',
        'payment_method',
        'created_at',
    ]

    list_filter = [
        'status',
        'payment_method',
        'created_at',
        'city',
    ]

    search_fields = [
        'order_number',
        'full_name',
        'mobile',
        'alternate_mobile',
        'email',
        'address',
    ]

    readonly_fields = [
        'order_number',
        'total_amount',
        'paid_amount',
        'created_at',
        'updated_at',
    ]

    # FIXED: Removed duplicate 'mobile'
    fieldsets = (
        ("Order Info", {
            'fields': ('order_number', 'status', 'payment_method', 'created_at')
        }),
        ("Customer", {
            'fields': ('full_name', 'mobile', 'alternate_mobile', 'email')
        }),
        ("Delivery Address", {
            'fields': ('address', 'landmark', 'city', 'pincode')
        }),
        ("Payment", {
            'fields': ('total_amount', 'paid_amount')
        }),
        ("Notes", {
            'fields': ('notes',)
        }),
    )

    ordering = ['-created_at']
    list_per_page = 50

    actions = [
        'mark_as_payment_done',
        'mark_as_confirmed',
        'mark_as_shipped',
        'mark_as_delivered'
    ]

    # Custom display
    def order_number_link(self, obj):
        return format_html(
            f'<a href="{obj.id}/change/" style="font-weight:bold; color:#1976d2;">{obj.order_number}</a>'
        )
    order_number_link.short_description = "Order No"

    def total_amount_colored(self, obj):
        color = "#d32f2f" if obj.total_amount > 1000 else "#2e7d32"
        return format_html(f'<span style="color:{color};font-weight:bold;">₹{obj.total_amount}</span>')
    total_amount_colored.short_description = "Total"

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'payment_done': '#4caf50',
            'confirmed': '#2196f3',
            'processing': '#ff9800',
            'shipped': '#9c27b0',
            'delivered': '#4caf50',
            'cancelled': '#f44336',
        }
        color = colors.get(obj.status, '#777')
        return format_html(
            f'<span style="background:{color};color:white;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:bold;">'
            f'{obj.get_status_display().upper()}'
            f'</span>'
        )
    status_badge.short_description = "Status"

    # Bulk Actions
    def mark_as_payment_done(self, request, queryset):
        updated = queryset.update(status='payment_done')
        self.message_user(request, f"{updated} order(s) marked as Payment Verified")
    mark_as_payment_done.short_description = "Mark as ₹5 Payment Verified"

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} order(s) confirmed")
    mark_as_confirmed.short_description = "Confirm selected orders"

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f"{updated} order(s) marked as Shipped")
    mark_as_shipped.short_description = "Mark as Shipped"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f"{updated} order(s) marked as Delivered")
    mark_as_delivered.short_description = "Mark as Delivered"


# Inline Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_purchase']
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


# Attach inline
OrderAdmin.inlines = [OrderItemInline]