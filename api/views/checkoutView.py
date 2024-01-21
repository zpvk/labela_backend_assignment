from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from datetime import datetime
from api.models.orderModel import Order
from api.models.cartModel import Cart
from api.serializers.orderSerializer import OrderSerializer

class CheckoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_cart = Cart.objects.get(user=request.user)
            delivery_date_str = request.data.get('delivery_date')
            
            # Validate and parse the delivery date
            try:
                delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

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