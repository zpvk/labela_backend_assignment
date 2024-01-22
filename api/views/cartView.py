from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from api.models.cartModel import Cart, CartItem
from api.models.productModel import Product
from api.serializers.cartSerializer import CartSerializer
from api.serializers.cartItemSerializer import CartItemSerializer
from rest_framework import status


class CartView(APIView):
    aauthentication_classes = [TokenAuthentication]
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

        response_data = {
            'status': 'success',
            'code': 200,  # Adjust the code as needed
            'message': "cart details",
            'data': cart_data,  # You can adjust this based on your needs
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.POST)
        user = request.user
        print("request user ", user.id)  # The user associated with the token
        user_cart, created = Cart.objects.get_or_create(user=user)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Validate that product_id and quantity are numbers
        if not (isinstance(product_id, int) and isinstance(quantity, int)):
            return Response({
                "errors": [
                    {
                        "status": "400",
                        "title": "Bad Request",
                        "detail": "Product ID and quantity must be numbers"
                    }
                ]
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Assuming you have a Product model with a 'price' field
            product = Product.objects.get(id=product_id)
            unit_price = product.price

        except Product.DoesNotExist:
            return Response({
                "errors": [
                    {
                        "status": "404",
                        "title": "Not Found",
                        "detail": "Product not found"
                    }
                ]
            }, status=status.HTTP_404_NOT_FOUND)

        user_cart.add_product(product_id, quantity)

        serializer = CartSerializer(user_cart)

        # You can customize the response content here
        response_data = {
            'status': 'success',
            'code': 201,  # Adjust the code as needed
            'message': f"Product '{product.name}' added to the cart successfully",
            'data': None,  # You can adjust this based on your needs
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            user_cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(id=product_id)

            is_available = self.check_product_availability(product_id)

            if is_available:
                user_cart.remove_product(product_id)
                response_data = {
                    'status': 'success',
                    'code': 201,  # Adjust the code as needed
                    'message': f"Product '{product.name}' removed from the cart successfully",
                    'data': None,  # You can adjust this based on your needs
                }
                return Response(response_data, status=status.HTTP_204_NO_CONTENT)
            else:
                response_data = {
                    'status': 'success',
                    'code': 404,  # Adjust the code as needed
                    'message': "Product not found in the cart",
                    'data': None,  # You can adjust this based on your needs
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        except Cart.DoesNotExist:
            response_data = {
                'status': 'success',
                'code': 404,  # Adjust the code as needed
                'message': "Cart not found",
                'data': None,  # You can adjust this based on your needs
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def check_product_availability(self, product_id):
        try:
            # Check if the product is in any cart item
            cart_item = CartItem.objects.get(product_id=product_id)
            return True
        except CartItem.DoesNotExist:
            return False
