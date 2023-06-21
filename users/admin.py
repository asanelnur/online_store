from django.contrib import admin

from users import models


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_superuser', 'is_staff']
    search_fields = ['username']


admin.site.register(models.CustomUser, UserAdmin)
