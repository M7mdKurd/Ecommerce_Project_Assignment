from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_items(self, request, *args, **kwargs):
        serializer = OrderSerializer(many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        order_serializer = OrderSerializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)

        item_serializer = OrderItemSerializer(data=request.data)
        item_serializer.is_valid(raise_exception=True)

        order, created = Order.objects.get_or_create(
            user_id=order_serializer.validated_data['user_id'],
            defaults={
            'tax': order_serializer.validated_data['tax'],
            'shipping_cost': order_serializer.validated_data['shipping_cost'],
            'order_status': order_serializer.validated_data['order_status'],
            'delivery_address': order_serializer.validated_data['delivery_address'],
            }
        )

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product_id=item_serializer.validated_data['product_id'],
            defaults={'quantity': item_serializer.validated_data['quantity']}
        )
        return Response(OrderItemSerializer(item).data, status=status.HTTP_201_CREATED)
