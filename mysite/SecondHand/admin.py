from django.contrib import admin
from .models import User,Category,Goods
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','time')

admin.site.register(User,UserAdmin)

admin.site.register(Category)

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name','description','trade_location','price','category','picture','seller','seller_phone','seller_qq','publish_time')

admin.site.register(Goods,GoodsAdmin)