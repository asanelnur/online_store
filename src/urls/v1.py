from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src import views

router = DefaultRouter()

router.register(r'products', views.ProductViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'order', views.OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
    path('basket/', views.BasketViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('basket/<pk>', views.BasketViewSet.as_view({'delete': 'destroy'})),
]
