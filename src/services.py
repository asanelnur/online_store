from typing import Protocol, OrderedDict

from django.db import transaction
from django.db.models import QuerySet

from src import models, repos
from users.models import CustomUser


class OrderServicesInterface(Protocol):

    def create_order(self, data: OrderedDict, user: CustomUser) -> models.Order: ...


    def get_orders(self, user: CustomUser) -> QuerySet[models.Order]: ...


class OrderServicesV1:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    def create_order(self, data: OrderedDict, user: CustomUser) -> models.Order:
        return self.order_repos.create_order(data=data, user=user)


    def get_orders(self, user: CustomUser) -> QuerySet[models.Order]:
        return self.order_repos.get_orders(user=user)
