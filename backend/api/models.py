"""Database models for ebike-shop.

Mirrors the schema.sql design but uses Django's ORM.
Money is stored as integer cents — never float.
"""

import uuid

from django.conf import settings
from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    class ProductType(models.TextChoices):
        EBIKE = "ebike", "E-Bike"
        PART = "part", "Part"
        ACCESSORY = "accessory", "Accessory"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price_cents = models.PositiveIntegerField()
    image_url = models.URLField(blank=True)
    product_type = models.CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.EBIKE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def price(self):
        """Return price as a decimal string for display."""
        return f"{self.price_cents / 100:.2f}"


class EbikeSpec(models.Model):
    """Extended specs only for ebike products. 1:1 with Product."""

    class FrameType(models.TextChoices):
        STEP_THRU = "step-thru", "Step-Thru"
        FAT_TIRE = "fat-tire", "Fat Tire"
        FOLDING = "folding", "Folding"
        STANDARD = "standard", "Standard"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True, related_name="ebike_spec"
    )
    motor_watts = models.PositiveIntegerField(null=True, blank=True)
    battery_wh = models.PositiveIntegerField(null=True, blank=True)
    range_miles = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    top_speed_mph = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    frame_type = models.CharField(
        max_length=20, choices=FrameType.choices, null=True, blank=True
    )
    weight_lbs = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    color_options = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Specs for {self.product.name}"


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    option_name = models.CharField(max_length=50, blank=True)
    option_value = models.CharField(max_length=100, blank=True)
    price_cents = models.PositiveIntegerField(null=True, blank=True)  # override product price
    stock_qty = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "option_name", "option_value")

    def __str__(self):
        return f"{self.product.name} — {self.option_name}: {self.option_value}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} ({self.user or 'guest'})"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product", "variant")

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "placed", "Placed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLACED
    )
    total_cents = models.PositiveIntegerField()
    shipping_name = models.CharField(max_length=200)
    shipping_addr1 = models.CharField(max_length=200)
    shipping_addr2 = models.CharField(max_length=200, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=20)
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

    @property
    def total(self):
        return f"{self.total_cents / 100:.2f}"


class OrderItem(models.Model):
    """Snapshot of purchased items — decoupled from cart so order
    history is immutable even if products change later."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_name = models.CharField(max_length=200)
    unit_price_cents = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"