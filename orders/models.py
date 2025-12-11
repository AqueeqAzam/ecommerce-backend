# orders/models.py → 100% MIGRATION-SAFE VERSION

from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator
import uuid


def generate_order_number():
    return f"ORD-{uuid.uuid4().hex.upper()[:10]}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('payment_done', 'Payment Done'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number, editable=False)

    # Customer Info → ALL HAVE DEFAULTS OR ALLOW BLANK
    full_name = models.CharField("Full Name", max_length=255, default="Not provided")
    mobile = models.CharField("Mobile Number", max_length=15, default="0000000000")
    alternate_mobile = models.CharField("Alternate Mobile", max_length=15, blank=True, default="")
    email = models.EmailField("Email (optional)", blank=True, null=True)

    # Delivery Info
    address = models.TextField("Delivery Address", default="Not provided")
    landmark = models.CharField("Landmark", max_length=200, blank=True, default="")
    city = models.CharField("City", max_length=100, default="Unknown City")
    pincode = models.CharField("Pincode", max_length=10, default="000000")

    # Extra
    notes = models.TextField("Special Instructions", blank=True, default="")

    # Payment & Status
    total_amount = models.DecimalField("Total Amount", max_digits=12, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField("Paid Amount", max_digits=10, decimal_places=2, default=5.00)
    payment_method = models.CharField(max_length=20, default="QR_SCAN", choices=[('QR_SCAN', '₹5 QR Payment')])
    payment_screenshot = models.ImageField(..., null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.full_name} ({self.mobile})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ← added default!

    def get_total(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"