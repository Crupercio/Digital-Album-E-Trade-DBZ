from django.contrib import admin
from . models import Category, CollectibleItem, Customer, Order, CustomerCollection, Album
# Register your models here.
admin.site.register(Category)
admin.site.register(CollectibleItem)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(CustomerCollection)
admin.site.register(Album)
