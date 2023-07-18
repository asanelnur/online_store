from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src import serializers, models, filters, permissions
from src.paginations import MyCustomPagination
from src.permissions import IsAdminOrReadOnly
from utils import mixins
from utils.mixins import ActionPermissionMixin


# Create your views here.


class ProductViewSet(mixins.ActionSerializerMixin, viewsets.ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.ProductRetrieveSerializer,
    }
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = MyCustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all().prefetch_related('products')
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        orders = models.Order.objects.filter(user_id=request.user.id)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = serializers.OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BasketViewSet(viewsets.ViewSet, ActionPermissionMixin):
    ACTION_PERMISSIONS = {
        'destroy': (permissions.IsOwnerOrAdmin(),),
    }
    permission_classes = IsAuthenticated,

    def list(self, request, *args, **kwargs):
        basket = models.Basket.objects.filter(user_id=request.user.id)
        serializer = serializers.BasketSerializer(basket, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.BasketCreateSerializer)
    def create(self, request, *args, **kwargs):
        serializer = serializers.BasketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, *args, **kwargs):
        instance = models.Basket.objects.get(id=kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
