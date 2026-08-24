from django.contrib.auth.models import User
from rest_framework import serializers

from orders.models import OrderItem, Order
from products.models import Products
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(source='item_total', max_digits=10, decimal_places=2, read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id',
                  'product_id',
                  'quantity',
                  'price',
                  'product',
                  ]

    # Validations

    def validate(self, attrs):
        if attrs['quantity'] > Products.objects.get(id=attrs['product_id']).stock:
            raise serializers.ValidationError("Out of Stock")

        return attrs

    def validate_product_id(self, value):
        try:
            Products.objects.get(id=value)
        except Products.DoesNotExist:
            raise serializers.ValidationError("Product Does Not Exist")
        return value



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)
    order_status = serializers.ChoiceField(choices=Order.order_status_choices, default='pending', read_only=True)

    class Meta:
        model = Order
        fields = ['id',
                  'user_id',
                  'created_at',
                  'updated_at',
                  'delivery_address',
                  'total_amount',
                  'order_status',
                  'items'
                  ]



    # Calculations

    def get_total_amount(self, obj):
        order_items = obj.items.all()
        return sum(order_items.item_total for order_items in order_items)






