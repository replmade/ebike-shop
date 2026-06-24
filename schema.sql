-- MySQL / PostgreSQL raw SQL reference schema
-- For this demo we use Django ORM + SQLite, but this file documents
-- the production schema for reference or manual setup.

CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name    TEXT,
    last_name     TEXT,
    created_at    TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE categories (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE products (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id   UUID REFERENCES categories(id),
    name          TEXT NOT NULL,
    slug          TEXT UNIQUE NOT NULL,
    description   TEXT,
    price_cents   INTEGER NOT NULL,
    image_url     TEXT,
    product_type  TEXT NOT NULL DEFAULT 'ebike',
    created_at    TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ebike_specs (
    product_id     UUID PRIMARY KEY REFERENCES products(id) ON DELETE CASCADE,
    motor_watts    INTEGER,
    battery_wh     INTEGER,
    range_miles    NUMERIC(5,1),
    top_speed_mph  NUMERIC(4,1),
    frame_type     TEXT,
    weight_lbs     NUMERIC(5,1),
    color_options   TEXT[]
);

CREATE TABLE product_variants (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id   UUID REFERENCES products(id) ON DELETE CASCADE,
    sku          TEXT UNIQUE,
    option_name  TEXT,
    option_value TEXT,
    price_cents  INTEGER,
    stock_qty    INTEGER DEFAULT 0,
    UNIQUE(product_id, option_name, option_value)
);

CREATE TABLE carts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id  TEXT,
    created_at  TIMESTAMPTZ DEFAULT now(),
    CHECK (user_id IS NOT NULL OR session_id IS NOT NULL)
);

CREATE TABLE cart_items (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id      UUID REFERENCES carts(id) ON DELETE CASCADE,
    product_id   UUID REFERENCES products(id) ON DELETE CASCADE,
    variant_id   UUID REFERENCES product_variants(id) ON DELETE CASCADE,
    quantity     INTEGER NOT NULL DEFAULT 1,
    added_at     TIMESTAMPTZ DEFAULT now(),
    UNIQUE(cart_id, product_id, variant_id)
);

CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    cart_id         UUID REFERENCES carts(id) ON DELETE SET NULL,
    status          TEXT DEFAULT 'placed',
    total_cents     INTEGER NOT NULL,
    shipping_name   TEXT NOT NULL,
    shipping_addr1  TEXT NOT NULL,
    shipping_addr2  TEXT,
    shipping_city   TEXT NOT NULL,
    shipping_state  TEXT NOT NULL,
    shipping_zip    TEXT NOT NULL,
    placed_at       TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE order_items (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id         UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id       UUID REFERENCES products(id) ON DELETE SET NULL,
    variant_id       UUID REFERENCES product_variants(id) ON DELETE SET NULL,
    product_name     TEXT NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    quantity         INTEGER NOT NULL
);