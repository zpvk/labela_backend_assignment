from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Cart, CartItem, Product
from decimal import Decimal
from datetime import date

class CartModelTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a product for testing
        self.product = Product.objects.create(name='Test Product', description='Test description', price=Decimal('10.00'))

    def test_add_product_to_cart(self):
        cart = Cart.objects.create(user=self.user)

        # Add a product to the cart
        cart.add_product(self.product.id, quantity=2)

        # Check if the CartItem was created and has the correct quantity and unit_price
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.unit_price, self.product.price)

    def test_remove_product_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart.add_product(self.product.id, quantity=3)

        # Remove the product from the cart
        cart.remove_product(self.product.id)

        # Check if the CartItem was removed
        self.assertEqual(cart.cartitem_set.count(), 0)

    def test_get_total_of_cart(self):
        cart = Cart.objects.create(user=self.user)

        # Add two products to the cart with different quantities
        cart.add_product(self.product.id, quantity=2)
        cart.add_product(self.product.id, quantity=3)

        # Check if the total is calculated correctly
        expected_total = 5 * self.product.price
        actual_total = cart.get_total()
        self.assertEqual(actual_total, expected_total)

    def test_get_total_of_empty_cart(self):
        cart = Cart.objects.create(user=self.user)

        # Check if the total of an empty cart is zero
        actual_total = cart.get_total()
        self.assertEqual(actual_total, Decimal('0.00'))
