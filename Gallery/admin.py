from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile,Painting,Cart,Order,Member
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CartInline(admin.StackedInline):
    model = Cart
    can_delete = False

class OrderInline(admin.StackedInline):
    model = Order
    can_delete = True


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,CartInline,OrderInline)



admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Painting)
admin.site.register(Member)
