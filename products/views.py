from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products import serializers
from products.models import Category, Products
from products.serializers import CategorySerializer, ProductSerializer



# Category ViewSet: Only has GET endpoint
# Items will be added from the database
class CategoryViewSet(viewsets.mixins.ListModelMixin,GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductViewSet(viewsets.ViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


    # Here we will use (POST/PUT/DELETE) only if its staff
    # We will add Authentication after we finish all the other things
    # I might change the structure again for this (no actions).

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
