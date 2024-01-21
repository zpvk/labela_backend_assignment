from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .models import Product, Cart, Order
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime
from .serializers import (
    ProductSerializer,
    UserSerializer,
    TokenResponseSerializer,
    ErrorResponseSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.serializer_class.Meta.model.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        serializer = TokenResponseSerializer({'token': token.key})
        return Response(serializer.data, status=200)

class CustomAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            serializer = TokenResponseSerializer({'token': token.key})
            return Response(serializer.data, status=200)
        
        else:
            # Use the custom serializer to format the error response
            error_serializer = ErrorResponseSerializer(data={
                'errors': [
                    {'title': 'Invalid Credentials', 'detail': 'Unable to log in with provided credentials.'}
                ]
            })
            if not error_serializer.is_valid():
                print(error_serializer.errors)

            return Response(error_serializer.data, status=status.HTTP_401_UNAUTHORIZED)


class ProductPagination(PageNumberPagination):
    default_page_size = 5

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size:
            return page_size
        return self.default_page_size

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

class AddToCartView(APIView):
    aauthentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print("request user ", user.id)  # The user associated with the token
        user_cart, created = Cart.objects.get_or_create(user=user.id)

        product_id = request.data.get('product_id')
        print("product id ", product_id)
        quantity = request.data.get('quantity')

        try:
            # Assuming you have a Product model with a 'price' field
            product = Product.objects.get(id=product_id)
            unit_price = product.price

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user_cart.add_product(product_id, quantity)

        serializer = CartSerializer(user_cart)

        # You can customize the response content here
        response_data = {
                'message': f"Product '{product.name}' added to the cart successfully"
            }
        return Response(response_data, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            user_cart = Cart.objects.get(user=request.user)
            user_cart.remove_product(product_id)
            return Response({'message': 'Product removed from the cart'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found in the cart'}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

class ViewCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_cart = Cart.objects.get(user=request.user)
        cart_items = user_cart.cartitem_set.all()  # Get all cart items associated with the user's cart
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        cart_data = {
            'cart_id': user_cart.id,
            'user_id': user_cart.user.id,
            'cart_items': cart_items_serializer.data,
            'total': user_cart.get_total(),  # Assuming you have a method to calculate the total
        }
        return Response(cart_data)
    
class CheckoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_cart = Cart.objects.get(user=request.user)
            delivery_date_str = request.data.get('delivery_date')
            
            # Validate and parse the delivery date
            delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()

            # Validate that delivery date is greater than the current date
            if delivery_date <= datetime.now().date():
                return Response({'error': 'Delivery date must be greater than the current date'}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total amount directly from the cart
            total_amount = user_cart.get_total()

            # Create an order
            order = Order.objects.create(user=request.user, delivery_date=delivery_date)

            # Move cart items to the order
            for cart_item in user_cart.cartitem_set.all():
                # Add each cart item to the order using add()
                order.cart_items.add(cart_item)

            # You can customize the response content here
            response_data = {
                'message': 'Order placed successfully',
                'total_amount': total_amount,
                'order_details': OrderSerializer(order).data,
            }
            # Remove all cart items from the cart
            user_cart.cartitem_set.all().delete()

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
