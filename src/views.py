from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src import serializers, models, filters, permissions, services
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
    order_services: services.OrderServicesInterface = services.OrderServicesV1()
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        orders = self.order_services.get_orders(user=request.user)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.OrderCreateSerializer)
    def create(self, request, *args, **kwargs):
        serializer = serializers.OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.order_services.create_order(serializer.validated_data, user=request.user )
        data = serializers.OrderSerializer(order).data
        return Response(data, status=status.HTTP_201_CREATED)

# {
#   "items": [
#     {
#       "product": "994815d5-2481-42e2-b564-8ed8ed43b462",
#       "count": 1
#     },
#     {
#       "product": "e0200b7f-7b76-46b3-a5aa-7f701d2eee9d",
#       "count": 2
#     }
#   ],
#   "total": "1500000"
# }
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
