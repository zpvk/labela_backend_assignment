from django.db import models
from django.contrib.auth.models import User
from .productModel import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def add_product(self, product_id, quantity):
        """
        Add a product to the cart.

        Args:
            product_id (int): ID of the product to be added.
            quantity (int): Quantity of the product to be added.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Product not found")

        # Create a new CartItem instance and associate it with the Cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity, 'unit_price': product.price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove_product(self, product_id):
        """
        Remove a product from the cart.

        Args:
            product_id (int): ID of the product to be removed.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Product not found")

        self.cartitem_set.filter(product=product).delete()

    def get_total(self):
        """
        Calculate the total cost of all products in the cart.

        Returns:
            Decimal: Total cost of products in the cart.
        """
        return sum(item.quantity * item.unit_price for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"CartItem {self.id} in {self.cart}"
