from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


    def get_items(self, request, *args, **kwargs):
        serializer = OrderSerializer(many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):

        cart = request.user.cart

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({'message': 'No items in cart '}, status=status.HTTP_400_BAD_REQUEST)

        if  Order.objects.filter(user=request.user).exists():
            return Response({'message': 'You have already placed an order'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.decrease_stock(item.quantity)

        cart.items.all().delete()


        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        order = Order.objects.get(id=pk)

        if order.order_status in ['shipping', 'delivered']:
            return Response({'message': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            order.order_status = 'cancelled'
            order.save()
            return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)




