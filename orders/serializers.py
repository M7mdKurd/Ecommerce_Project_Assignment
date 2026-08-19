from django.contrib.auth.models import User
from rest_framework import serializers

from orders.models import OrderItem, Order
from products.models import Products


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='item_total', max_digits=10, decimal_places=2, read_only=True)
    product_description = serializers.CharField(source='product.description', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id',
                  'product_id',
                  'quantity',
                  'price',
                  'product_name',
                  'product_description',
                  'product_image'
                  ]

    def validate(self, attrs):
        if attrs['quantity'] > Products.objects.get(id=attrs['product_id']).stock:
            raise serializers.ValidationError("Out of Stock")

        try:
            Products.objects.get(id=attrs['product_id'])
        except Products.DoesNotExist:
            raise serializers.ValidationError("Invalid Product")


        return attrs



class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.05)
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    grand_total = serializers.SerializerMethodField(read_only=True)
    order_status = serializers.ChoiceField(choices=Order.order_status_choices, default='pending')

    class Meta:
        model = Order
        fields = ['id',
                  'user_id',
                  'created_at',
                  'updated_at',
                  'delivery_address',
                  'total_amount',
                  'tax',
                  'shipping_cost',
                  'grand_total',
                  'order_status',
                  'items'
                  ]


    def get_total_amount(self, obj):
        order_items = obj.items.all()
        return sum(order_items.item_total for order_items in order_items)

    def get_grand_total(self, obj):
        tax_money = self.get_total_amount(obj) * obj.tax
        return self.get_total_amount(obj) + tax_money + obj.shipping_cost

    def validate(self, attrs):
        try:
            User.objects.get(id=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User")

        return attrs




