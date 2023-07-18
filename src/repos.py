from typing import Protocol, OrderedDict

from django.db import transaction
from django.db.models import QuerySet

from src import models
from users.models import CustomUser


class OrderReposInterface(Protocol):

    @staticmethod
    def create_order(data: OrderedDict, user: CustomUser) -> models.Order: ...

    @staticmethod
    def get_orders(user: CustomUser) -> QuerySet[models.Order]: ...


class OrderReposV1:

    @staticmethod
    def create_order(data: OrderedDict, user: CustomUser) -> models.Order:
        with transaction.atomic():
            order_items = data.pop('items')

            order = models.Order.objects.create(**data, user=user)

            models.OrderItem.objects.bulk_create([
                models.OrderItem(
                    order=order,
                    product=i['product'],
                    count=i['count'],
                ) for i in order_items
            ])

        return order

    @staticmethod
    def get_orders(user: CustomUser) -> QuerySet[models.Order]:
        if user.is_staff:
            return models.Order.objects.all()
        return models.Order.objects.filter(user=user)
