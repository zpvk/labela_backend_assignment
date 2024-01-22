from rest_framework import serializers
from api.serializers.cartItemSerializer import CartItemSerializer
from api.models.cartModel import Cart, CartItem
from api.models.productModel import Product


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'items']

    def create(self, validated_data):
        # Create or update cart items
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)

        for item_data in items_data:
            product_data = item_data.pop('product')
            product = Product.objects.get_or_create(**product_data)[0]

            CartItem.objects.create(cart=cart, product=product, **item_data)

        return cart
