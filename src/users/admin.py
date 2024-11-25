from django.contrib import admin


from src.auction.models import Address
from src.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'email', 'phone', 'address', 'is_active', 'is_staff')
    search_fields = ('full_name', 'username', 'email', 'phone')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)

admin.site.register(Address)
