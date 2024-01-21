from rest_framework import serializers
from .models import Product, CartItem, Cart, Order
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']

    def to_representation(self, instance):
        # Customize the representation if needed
        representation = super().to_representation(instance)
        # You can add more customization here if needed
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username', 'password']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class TokenResponseSerializer(serializers.Serializer):
    class Meta:
        fields = ('token',)

    def to_representation(self, instance):
        return {
            'data': {
                'type': 'tokens',
                'attributes': {
                    'token': instance['token']
                }
            }
        }

class ErrorDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    detail = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    errors = ErrorDetailSerializer(many=True)

    def to_representation(self, instance):
        return {
            'errors': instance['errors']
        }
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'unit_price']

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

class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'