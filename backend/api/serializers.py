"""DRF serializers for the ebike-shop API."""

from rest_framework import serializers

from .models import (
    Cart,
    CartItem,
    Category,
    EbikeSpec,
    Order,
    OrderItem,
    Product,
    ProductVariant,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class EbikeSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = EbikeSpec
        fields = [
            "motor_watts",
            "battery_wh",
            "range_miles",
            "top_speed_mph",
            "frame_type",
            "weight_lbs",
            "color_options",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "sku", "option_name", "option_value", "price_cents", "stock_qty"]


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    ebike_spec = EbikeSpecSerializer(read_only=True)
    price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "description",
            "price_cents",
            "price",
            "image_url",
            "product_type",
            "variants",
            "ebike_spec",
            "created_at",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    variant_id = serializers.UUIDField(write_only=True, required=False)
    line_total_cents = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "variant",
            "product_id",
            "variant_id",
            "quantity",
            "line_total_cents",
            "added_at",
        ]

    def get_line_total_cents(self, obj):
        unit = obj.variant.price_cents if obj.variant and obj.variant.price_cents else obj.product.price_cents
        return unit * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "session_id", "items", "created_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "unit_price_cents", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_cents",
            "total",
            "shipping_name",
            "shipping_addr1",
            "shipping_addr2",
            "shipping_city",
            "shipping_state",
            "shipping_zip",
            "items",
            "placed_at",
        ]