"""API URL routes for ebike-shop."""

from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    CartItemView,
    CartView,
    CategoryListView,
    CheckoutView,
    LoginView,
    ProductDetailView,
    ProductListView,
    RegisterView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/items/<uuid:item_id>/", CartItemView.as_view(), name="cart-item"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
]