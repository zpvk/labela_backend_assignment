from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from api.models.productModel import Product
from .productPagination import ProductPagination
from api.serializers.productSerializer import ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # No authentication required for product listing
    

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser] # Only admin users can add products
    authentication_classes = (TokenAuthentication,) 

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]  # No authentication required for product detail view