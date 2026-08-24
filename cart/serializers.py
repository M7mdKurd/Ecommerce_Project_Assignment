from django.contrib.auth.models import User
from rest_framework import serializers

from cart.models import CartItem, Cart
from products.models import Products
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product = ProductSerializer(read_only=True)
    price = serializers.DecimalField(source='item_total', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
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



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()


    class Meta:
        model = Cart
        fields = ['id',
                  'created_at',
                  'total_amount',
                  'items'
                  ]


    def get_total_amount(self,obj):
        cart_items = obj.items.all()
        return sum(cart_items.item_total for cart_items in cart_items)
