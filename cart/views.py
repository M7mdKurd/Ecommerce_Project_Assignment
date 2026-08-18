from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_items(self, request, *args, **kwargs):
        serializer = CartSerializer(many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add')
    def add_item(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializers = CartSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        cart, created = Cart.objects.get_or_create(user_id=serializers.validated_data['user_id'])


        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=serializer.validated_data['product_id'],
            defaults={'quantity': serializer.validated_data['quantity']}
        )


        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_item(self, request, pk=None):
        Cart.objects.filter(id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['put'], url_path='update')
    def update_quantity(self, request, pk=None):
        serializers = CartItemSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        cart_item = CartItem.objects.get(id=pk)
        cart_item.quantity = request.data.get('quantity',cart_item.quantity)
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        Cart.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

