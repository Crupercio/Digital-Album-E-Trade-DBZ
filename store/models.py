from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Album Model
class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# Combined Product and Sticker Model
class CollectibleItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, default='', blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    image = models.ImageField(upload_to='uploads/collectibles/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    
    # Sale and trade status
    is_sale = models.BooleanField(default=True)  # Can be listed for sale
    is_tradeable = models.BooleanField(default=True)  # Tradeable unless collected
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    
    # Album-specific properties
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="collectibles")  # Track the album it belongs to
    page_number = models.IntegerField()  # For organizing in album
    position_on_page = models.IntegerField()  # Position slot on the page

    def __str__(self):
        return self.name


# Track customer collection and ownership
class CustomerCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(CollectibleItem, on_delete=models.CASCADE)
    owned = models.BooleanField(default=False)  # If the item is owned but not yet collected
    collected = models.BooleanField(default=False)  # If the item is collected
    tradeable = models.BooleanField(default=True)  # Tradeable unless collected

    def mark_as_collected(self):
        self.collected = True
        self.owned = False  # It's no longer just owned, it's collected
        self.tradeable = False  # Once collected, it can no longer be traded
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.item.name} - {'Collected' if self.collected else 'Owned' if self.owned else 'Available'}"

# Customer Orders for purchased items
class Order(models.Model):
    item = models.ForeignKey(CollectibleItem, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(default=datetime.datetime.today)
    shipped_status = models.BooleanField(default=False)  # Tracks if the order has been completed

    def __str__(self):
        return f"Order of {self.item.name} by {self.customer.username}"

    # Mark the item as collected after the order is shipped
    def mark_as_collected(self):
        collection, created = CustomerCollection.objects.get_or_create(user=self.customer, item=self.item)
        collection.collected = True
        collection.tradeable = False  # Once collected, it's no longer tradeable
        collection.save()


