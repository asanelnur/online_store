from rest_framework import serializers

from src import models


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = '__all__'


class _ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    images = _ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = models.OrderItem
        fields = ('title', 'price', 'count', 'total_price')


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'





class BasketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Basket
        fields = ('product',)


class BasketProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('title', 'desc', 'price')


class BasketSerializer(serializers.ModelSerializer):
    product = BasketProductSerializer(read_only=True)

    class Meta:
        model = models.Basket
        fields = '__all__'
