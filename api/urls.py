from django.urls import path, re_path
from api.views.userRegistrationView import UserRegistrationView
from api.views.productView import ProductListCreateView, ProductListView, ProductDetailView
from api.views.cartView import AddToCartView, RemoveFromCartView, ViewCartView
from api.views.customAuthTokenView import CustomAuthTokenView
from api.views.checkoutView import CheckoutView
from api.views.notFoundView import NotFoundView

from django.views.generic import TemplateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('products/', ProductListView.as_view(), name='product-list-view'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('admin/products/', ProductListCreateView.as_view(), name='admin-product-list-create'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/view/', ViewCartView.as_view(), name='view-cart'),
    path('api-token-auth/', CustomAuthTokenView.as_view(), name='custom_api_token_auth'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html',extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    re_path(r'^.*$', NotFoundView.as_view()),
    
]