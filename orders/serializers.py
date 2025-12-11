# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'product_price', 'quantity', 'price_at_purchase']
        read_only_fields = ['price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(many=True, source='items', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'full_name',
            'mobile',
            'alternate_mobile',
            'email',
            'address',
            'landmark',
            'city',
            'pincode',
            'notes',
            'items',           # for creating
            'order_items',     # for reading
            'total_amount',
            'paid_amount',     # always 5.00
            'payment_screenshot',
            'status',
            'created_at',
        ]
        read_only_fields = [
            'id', 'order_number', 'total_amount', 'paid_amount',
            'status', 'created_at', 'order_items'
        ]

    def get_total_amount(self, obj):
        return sum(item.get_total() for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Force paid_amount = ₹5
        validated_data['paid_amount'] = 5.00
        validated_data['payment_method'] = 'QR_SCAN'

        order = Order.objects.create(**validated_data)

        total = 0
        for item_data in items_data:
            product = item_data['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price_at_purchase=product.price
            )
            total += product.price * item_data['quantity']

        order.total_amount = total
        order.save()
        return order