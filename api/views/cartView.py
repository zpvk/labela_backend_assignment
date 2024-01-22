from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from api.models.cartModel import Cart
from api.models.productModel import Product
from api.serializers.cartSerializer import CartSerializer
from api.serializers.cartItemSerializer import CartItemSerializer
from rest_framework import status

class AddToCartView(APIView):
    aauthentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.POST)
        user = request.user
        print("request user ", user.id)  # The user associated with the token
        user_cart, created = Cart.objects.get_or_create(user=user)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

         # Validate that product_id and quantity are numbers
        if not (isinstance(product_id, int) and isinstance(quantity, int)):
            return Response({'error': 'Product ID and quantity must be numbers'}, status=status.HTTP_400_BAD_REQUEST)

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