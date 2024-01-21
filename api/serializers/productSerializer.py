from rest_framework import serializers
from api.models.productModel import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']

    def to_representation(self, instance):
        # Customize the representation if needed
        representation = super().to_representation(instance)
        # You can add more customization here if needed
        return representation