from django.contrib import admin
from .models import Product, User, Favourites, OrderItem
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Favourites)
admin.site.register(OrderItem)