from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

# 보여지는 형태가 다름
# class UserInline(admin.StackedInline):
class UserInline(admin.TabularInline):
    model = User.followings.through
    fk_name = 'from_user'

class CustomUserAdmin(UserAdmin):
    inlines = [UserInline]
    
admin.site.register(User, CustomUserAdmin)