from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)


    def create(self, request, *args, **kwargs):

        try:
            cart = request.user.cart
        except ObjectDoesNotExist:
            return Response({'message': 'You have no Cart Active'}, status=status.HTTP_400_BAD_REQUEST)


        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({'message': 'No items in cart'}, status=status.HTTP_400_BAD_REQUEST)


        if Order.objects.filter(user=request.user).exclude(order_status__in=['delivered', 'cancelled']).exists():
            return Response({'message': 'You have already placed an order'}, status=status.HTTP_400_BAD_REQUEST)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.decrease_stock(item.quantity)

        cart_items.delete()


        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):

        order = self.get_object()

        if order.order_status == 'cancelled':
            return Response({'message': 'Order already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        if order.order_status in ['shipping', 'delivered']:
            return Response({'message': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            order.order_status = 'cancelled'
            order.save()

            for item in order.items.all():
                item.product.increase_stock(item.quantity)
            return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)