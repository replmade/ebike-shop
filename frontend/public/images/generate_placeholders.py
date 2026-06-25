#!/usr/bin/env python3
"""Generate professional product placeholder images for VoltCycle demo."""
from PIL import Image, ImageDraw, ImageFont
import os

# Brand colors
BG_DARK = (26, 26, 26)
BG_GRADIENT_END = (45, 45, 45)
ACCENT = (232, 185, 35)  # #e8b923
WHITE = (255, 255, 255)
GRAY = (136, 136, 136)
LIGHT_GRAY = (200, 200, 200)

PRODUCTS = [
    # (filename, title, subtitle, icon_symbol)
    ("voltrider-commuter.jpg", "VoltRider", "Commuter", "⚡", "Electric City Bike"),
    ("trailblazer-fat-tire.jpg", "Trailblazer", "Fat Tire", "🏔️", "Off-Road EBike"),
    ("cityglide-folding.jpg", "CityGlide", "Folding", "🔄", "Compact Folding EBike"),
    ("48v-battery.jpg", "48V 15Ah", "Battery", "🔋", "Replacement Battery"),
    ("36v-battery.jpg", "36V 10Ah", "Battery", "🔋", "Replacement Battery"),
    ("charger-48v.jpg", "48V Smart", "Charger", "🔌", "Battery Charger"),
    ("helmet.jpg", "VoltCycle", "Helmet", "🪖", "Urban Cycling Helmet"),
    ("u-lock.jpg", "Heavy-Duty", "U-Lock", "🔒", "Hardened Steel Lock"),
    ("cargo-rack.jpg", "Rear Cargo", "Rack", "📦", "Aluminum Cargo Rack"),
    ("front-basket.jpg", "Front", "Basket", "🧺", "Wicker-Style Basket"),
    ("ebike-cover.jpg", "Waterproof", "Cover", "🌧️", "Full-Coverage Cover"),
]

def create_gradient(draw, width, height):
    """Draw a subtle diagonal gradient."""
    for y in range(height):
        ratio = y / height
        r = int(BG_DARK[0] + (BG_GRADIENT_END[0] - BG_DARK[0]) * ratio)
        g = int(BG_DARK[1] + (BG_GRADIENT_END[1] - BG_DARK[1]) * ratio)
        b = int(BG_DARK[2] + (BG_GRADIENT_END[2] - BG_DARK[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_bike_icon(draw, cx, cy, size, color):
    """Draw a simple bike icon."""
    s = size
    # Wheels
    draw.ellipse([cx - s*0.4, cy - s*0.1, cx - s*0.1, cy + s*0.2], outline=color, width=3)
    draw.ellipse([cx + s*0.1, cy - s*0.1, cx + s*0.4, cy + s*0.2], outline=color, width=3)
    # Frame
    draw.line([(cx - s*0.25, cy + s*0.05), (cx, cy - s*0.25), (cx + s*0.25, cy + s*0.05)], fill=color, width=3)
    draw.line([(cx, cy - s*0.25), (cx + s*0.15, cy - s*0.25)], fill=color, width=3)
    # Handlebar
    draw.line([(cx + s*0.15, cy - s*0.25), (cx + s*0.2, cy - s*0.3)], fill=color, width=3)
    # Seat
    draw.line([(cx - s*0.05, cy - s*0.28), (cx + s*0.05, cy - s*0.28)], fill=color, width=3)

def draw_battery_icon(draw, cx, cy, size, color):
    """Draw a battery icon."""
    s = size
    # Battery body
    draw.rounded_rectangle([cx - s*0.3, cy - s*0.2, cx + s*0.2, cy + s*0.2], radius=5, outline=color, width=3)
    # Battery terminal
    draw.rounded_rectangle([cx + s*0.2, cy - s*0.08, cx + s*0.3, cy + s*0.08], radius=3, outline=color, width=2)
    # Charge bars
    draw.rectangle([cx - s*0.22, cy - s*0.12, cx - s*0.1, cy + s*0.12], fill=color)
    draw.rectangle([cx - s*0.05, cy - s*0.12, cx + s*0.07, cy + s*0.12], fill=color)

def draw_lock_icon(draw, cx, cy, size, color):
    """Draw a U-lock icon."""
    s = size
    # U shape
    draw.arc([cx - s*0.2, cy - s*0.35, cx + s*0.2, cy + s*0.05], start=180, end=360, fill=color, width=4)
    draw.line([(cx - s*0.2, cy), (cx - s*0.2, cy + s*0.2)], fill=color, width=4)
    draw.line([(cx + s*0.2, cy), (cx + s*0.2, cy + s*0.2)], fill=color, width=4)
    # Crossbar
    draw.rectangle([cx - s*0.25, cy + s*0.15, cx + s*0.25, cy + s*0.25], outline=color, width=2)

def draw_helmet_icon(draw, cx, cy, size, color):
    """Draw a helmet icon."""
    s = size
    draw.arc([cx - s*0.3, cy - s*0.25, cx + s*0.3, cy + s*0.2], start=180, end=360, fill=color, width=3)
    draw.line([(cx - s*0.3, cy), (cx + s*0.3, cy)], fill=color, width=3)
    draw.line([(cx - s*0.2, cy), (cx - s*0.25, cy + s*0.15)], fill=color, width=2)
    draw.line([(cx + s*0.2, cy), (cx + s*0.25, cy + s*0.15)], fill=color, width=2)

def draw_box_icon(draw, cx, cy, size, color):
    """Draw a box/rack icon."""
    s = size
    draw.rectangle([cx - s*0.25, cy - s*0.2, cx + s*0.25, cy + s*0.2], outline=color, width=3)
    draw.line([(cx - s*0.25, cy - s*0.05), (cx + s*0.25, cy - s*0.05)], fill=color, width=2)
    # Grid lines
    draw.line([(cx, cy - s*0.2), (cx, cy + s*0.2)], fill=color, width=1)

def draw_shield_icon(draw, cx, cy, size, color):
    """Draw a cover/shield icon."""
    s = size
    draw.pieslice([cx - s*0.3, cy - s*0.3, cx + s*0.3, cy + s*0.3], start=180, end=360, fill=None, outline=color, width=3)
    draw.line([(cx - s*0.3, cy), (cx + s*0.3, cy)], fill=color, width=3)
    # Drip lines
    for x_off in [-0.15, 0, 0.15]:
        draw.line([(cx + int(s*x_off), cy), (cx + int(s*x_off), cy + s*0.15)], fill=ACCENT, width=2)

ICON_MAP = {
    "⚡": draw_bike_icon,
    "🏔️": draw_bike_icon,
    "🔄": draw_bike_icon,
    "🔋": draw_battery_icon,
    "🔌": draw_battery_icon,
    "🪖": draw_helmet_icon,
    "🔒": draw_lock_icon,
    "📦": draw_box_icon,
    "🧺": draw_box_icon,
    "🌧️": draw_shield_icon,
}

# Try to find a font
font_paths = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SFNSDisplay.ttf",
    "/System/Library/Fonts/SFNSText.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]

font_large = None
font_medium = None
font_small = None

for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_large = ImageFont.truetype(fp, 36)
            font_medium = ImageFont.truetype(fp, 22)
            font_small = ImageFont.truetype(fp, 16)
            break
        except Exception:
            continue

if font_large is None:
    # Use default
    font_large = ImageFont.load_default()
    font_medium = font_large
    font_small = font_large

output_dir = os.path.dirname(os.path.abspath(__file__))

for filename, title, subtitle, icon, desc in PRODUCTS:
    img = Image.new("RGB", (600, 400), BG_DARK)
    draw = ImageDraw.Draw(img)
    create_gradient(draw, 600, 400)
    
    # Decorative accent line at top
    draw.rectangle([0, 0, 600, 4], fill=ACCENT)
    
    # Draw product icon
    icon_fn = ICON_MAP.get(icon, draw_bike_icon)
    icon_fn(draw, 300, 150, 200, ACCENT)
    
    # Product name
    draw.text((300, 250), title, fill=WHITE, font=font_large, anchor="mm")
    draw.text((300, 285), subtitle, fill=ACCENT, font=font_medium, anchor="mm")
    
    # Description
    draw.text((300, 330), desc, fill=GRAY, font=font_small, anchor="mm")
    
    # Bottom accent line
    draw.rectangle([0, 396, 600, 400], fill=ACCENT)
    
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, "JPEG", quality=85)
    print(f"Created {filename} ({os.path.getsize(filepath)} bytes)")

print("\nAll product images generated!")