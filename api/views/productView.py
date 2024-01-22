from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from api.views.productPagination import ProductPagination
from api.models.productModel import Product
from .productPagination import ProductPagination
from api.serializers.productSerializer import ProductSerializer


class ProductListView(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')  # Order by the product's primary key
    pagination_class = ProductPagination
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]  # No authentication required for product detail view


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]  # No authentication required for product detail view

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = {
            'status': 'success',
            'code': 200,
            'message': 'OK',
            'data': serializer.data
        }

        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        response_data = {
            'status': 'success',
            'code': 200,  # 204 for successful deletion
            'message': 'Product deleted successfully'
        }

        return Response(response_data, status=200)
