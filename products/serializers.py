from rest_framework import serializers

from products.models import Products, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id, name, description, count_products'



class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()


    class Meta:
        model = Products
        fields = (
            'id',
            'category_id',
            'name',
            'description',
            'price',
            'image',
        )


        def validate(self, attrs):
            if attrs['stock'] < 1:
                raise serializers.ValidationError('Stock must be greater than 0')

            try:
                Category.objects.get(id=attrs['category_id'])
            except Category.DoesNotExist:
                raise serializers.ValidationError('Invalid category')

            if attrs['price'] < 0:
                raise serializers.ValidationError('Price must be greater than 0')

            return attrs


