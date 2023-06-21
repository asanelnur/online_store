import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from onlinestore import settings


# Create your models here.


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('title',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    main_image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name=_('Main image'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))
    is_top = models.BooleanField(default=False, verbose_name=_('Is top?'))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='products')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('is_top', '-created_at')
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    product = models.ForeignKey(to=Product,
                                on_delete=models.CASCADE,
                                related_name='images',
                                verbose_name=_('Product'))
    image = models.ImageField(upload_to='product-images/%Y/%m/%d/', verbose_name=_('Image'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.title

    @property
    def title(self):
        return self.product.title

    @property
    def price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price*self.count


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(to=OrderItem)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.user} {self.created_at}'


class Basket(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s basket"
