from rest_framework import serializers
from api.models.cartModel import CartItem
from api.serializers.productSerializer import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'unit_price']