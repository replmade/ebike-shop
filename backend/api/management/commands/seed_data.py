"""Seed command to populate demo data.

Usage: python manage.py seed_data
"""

import decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from api.models import Category, EbikeSpec, Product


class Command(BaseCommand):
    help = "Seed the database with demo ebike shop data"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create demo user
        if not User.objects.filter(username="demo@voltcycle.com").exists():
            User.objects.create_user(
                username="demo@voltcycle.com",
                email="demo@voltcycle.com",
                password="demo1234",
                first_name="Demo",
                last_name="Rider",
            )
            self.stdout.write("Created demo user (demo@voltcycle.com / demo1234)")

        # Categories
        cat_ebikes, _ = Category.objects.get_or_create(
            slug="ebikes",
            defaults={"name": "E-Bikes", "description": "Electric bicycles"},
        )
        cat_parts, _ = Category.objects.get_or_create(
            slug="parts",
            defaults={"name": "Parts", "description": "Replacement parts and batteries"},
        )
        cat_accessories, _ = Category.objects.get_or_create(
            slug="accessories",
            defaults={"name": "Accessories", "description": "Helmets, locks, racks, and gear"},
        )

        # --- 3 Ebike models ---
        ebike1, created = Product.objects.get_or_create(
            slug="voltrider-commuter",
            defaults={
                "category": cat_ebikes,
                "name": "VoltRider Commuter",
                "description": "Sleek city commuter with smooth pedal assist. Perfect for daily urban rides.",
                "price_cents": 189900,
                "image_url": "https://placehold.co/600x400/1a1a1a/e8b923?text=VoltRider+Commuter",
                "product_type": "ebike",
            },
        )
        if created:
            EbikeSpec.objects.create(
                product=ebike1,
                motor_watts=350,
                battery_wh=480,
                range_miles=decimal.Decimal("45.0"),
                top_speed_mph=decimal.Decimal("20.0"),
                frame_type="step-thru",
                weight_lbs=decimal.Decimal("48.0"),
                color_options=["matte black", "pearl white", "steel blue"],
            )
            self.stdout.write("Created VoltRider Commuter")

        ebike2, created = Product.objects.get_or_create(
            slug="trailblazer-fat-tire",
            defaults={
                "category": cat_ebikes,
                "name": "Trailblazer Fat Tire",
                "description": "Off-road ready with fat tires and a powerful motor for trails and sand.",
                "price_cents": 229900,
                "image_url": "https://placehold.co/600x400/1a1a1a/e8b923?text=Trailblazer+Fat+Tire",
                "product_type": "ebike",
            },
        )
        if created:
            EbikeSpec.objects.create(
                product=ebike2,
                motor_watts=750,
                battery_wh=672,
                range_miles=decimal.Decimal("35.0"),
                top_speed_mph=decimal.Decimal("28.0"),
                frame_type="fat-tire",
                weight_lbs=decimal.Decimal("68.0"),
                color_options=["matte black", "olive green", "sand"],
            )
            self.stdout.write("Created Trailblazer Fat Tire")

        ebike3, created = Product.objects.get_or_create(
            slug="cityglide-folding",
            defaults={
                "category": cat_ebikes,
                "name": "CityGlide Folding",
                "description": "Compact folding ebike for commuters with limited storage space.",
                "price_cents": 149900,
                "image_url": "https://placehold.co/600x400/1a1a1a/e8b923?text=CityGlide+Folding",
                "product_type": "ebike",
            },
        )
        if created:
            EbikeSpec.objects.create(
                product=ebike3,
                motor_watts=250,
                battery_wh=360,
                range_miles=decimal.Decimal("30.0"),
                top_speed_mph=decimal.Decimal("15.5"),
                frame_type="folding",
                weight_lbs=decimal.Decimal("38.0"),
                color_options=["white", "charcoal", "red"],
            )
            self.stdout.write("Created CityGlide Folding")

        # --- Parts (replacement batteries) ---
        Product.objects.get_or_create(
            slug="48v-15ah-replacement-battery",
            defaults={
                "category": cat_parts,
                "name": "48V 15Ah Replacement Battery",
                "description": "Compatible with VoltRider and Trailblazer models. 720Wh capacity.",
                "price_cents": 44900,
                "image_url": "https://placehold.co/600x400/eee/1a1a1a?text=48V+15Ah+Battery",
                "product_type": "part",
            },
        )
        Product.objects.get_or_create(
            slug="36v-10ah-replacement-battery",
            defaults={
                "category": cat_parts,
                "name": "36V 10Ah Replacement Battery",
                "description": "Compatible with CityGlide Folding. 360Wh capacity.",
                "price_cents": 29900,
                "image_url": "https://placehold.co/600x400/eee/1a1a1a?text=36V+10Ah+Battery",
                "product_type": "part",
            },
        )
        Product.objects.get_or_create(
            slug="replacement-charger-48v",
            defaults={
                "category": cat_parts,
                "name": "48V Smart Charger",
                "description": "Replacement charger for 48V battery systems. LED charge indicator.",
                "price_cents": 7900,
                "image_url": "https://placehold.co/600x400/eee/1a1a1a?text=48V+Charger",
                "product_type": "part",
            },
        )
        self.stdout.write("Created replacement batteries and charger")

        # --- Accessories ---
        accessories = [
            ("voltcycle-helmet", "VoltCycle Helmet", "Certified urban cycling helmet with LED tail light.", 5900),
            ("heavy-duty-u-lock", "Heavy-Duty U-Lock", "Hardened steel U-lock with mounting bracket.", 3900),
            ("rear-cargo-rack", "Rear Cargo Rack", "Aluminum cargo rack, compatible with all VoltCycle models.", 6900),
            ("front-basket", "Front Basket", "Wicker-style front basket for commuting essentials.", 4500),
            ("ebike-cover", "Waterproof E-Bike Cover", "Full-coverage waterproof cover for outdoor storage.", 3500),
        ]
        for slug, name, desc, price in accessories:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": cat_accessories,
                    "name": name,
                    "description": desc,
                    "price_cents": price,
                    "image_url": f"https://placehold.co/600x400/eee/1a1a1a?text={name.replace(' ', '+')}",
                    "product_type": "accessory",
                },
            )
        self.stdout.write("Created accessories")

        self.stdout.write(self.style.SUCCESS("Seed complete!"))