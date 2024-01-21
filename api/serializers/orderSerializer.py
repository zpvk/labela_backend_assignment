from rest_framework import serializers
from api.serializers.cartItemSerializer import CartItemSerializer
from api.models.orderModel import Order


class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'