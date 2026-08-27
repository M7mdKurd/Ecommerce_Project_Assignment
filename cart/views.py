from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add')
    def add_item(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        cart, created = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}

        )

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['delete'], url_path='items')
    def delete_item(self, request, pk=None):

        try:
            self.get_object().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['put'], url_path='update')
    def update_quantity(self, request, pk=None):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart.objects.get(id=pk, user=request.user)
        item = cart.items.get(product_id=serializer.validated_data['product_id'])
        item.quantity = serializer.validated_data['quantity']
        item.save()

        return Response(CartItemSerializer(item).data)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

