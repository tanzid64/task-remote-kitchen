from django.db import models
from core.models import TimeStampMixin
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Restaurant(TimeStampMixin):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant")
    restaurant_name = models.CharField(verbose_name=_("Restaurant Name"), max_length=100)
    slug = AutoSlugField(populate_from="restaurant_name", unique=True) 
    address = models.CharField(verbose_name=_("Address"), max_length=100)
    employees = models.ManyToManyField(User, related_name="employees", blank=True, null=True)

    def __str__(self):
        return self.restaurant_name
    
class Menu(TimeStampMixin):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True) 
    details = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{self.restaurant.restaurant_name} - {self.name}"
    
class Item(TimeStampMixin):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="item_name", unique=True) 
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.item_name}-{self.menu.name}"
