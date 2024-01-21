from django.db import models
from django.contrib.auth.models import User
from .cartModel import CartItem

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem, related_name='orders')
    delivery_date = models.DateField()

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
