from django.contrib import admin

from src import models


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1




class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_top', 'is_active')
    list_filter = ('is_top', 'is_active')
    list_editable = ('is_top', 'is_active')
    search_fields = ('title', 'body')
    inlines = (ProductImageInline,)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductImage)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
admin.site.register(models.Category)
admin.site.register(models.Basket)