import { test, expect } from "@playwright/test";

function makeTestUser() {
  const id = Date.now() + Math.random().toString(36).slice(2, 6);
  return {
    email: "test_" + id + "@example.com",
    password: "TestPass123!",
    firstName: "Test",
    lastName: "User",
  };
}

async function registerUser(request, user) {
  const response = await request.post("/api/auth/register/", {
    data: {
      email: user.email,
      password: user.password,
      first_name: user.firstName,
      last_name: user.lastName,
    },
  });
  expect(response.status()).toBe(201);
  return response.json();
}

async function loginUser(request, user) {
  const response = await request.post("/api/auth/login/", {
    data: { email: user.email, password: user.password },
  });
  expect(response.status()).toBe(200);
  return response.json();
}

function authHeaders(token) {
  return { Authorization: "Token " + token };
}

// ─── Cart API tests ─────────────────────────────────────────────────────────

test.describe("Cart API", () => {
  test("guest can add a product to cart", async ({ request }) => {
    const productsRes = await request.get("/api/products/?type=part");
    expect(productsRes.status()).toBe(200);
    const products = await productsRes.json();
    expect(products.length).toBeGreaterThan(0);
    const productId = products[0].id;

    const addRes = await request.post("/api/cart/", {
      data: { product_id: productId, quantity: 1 },
    });
    expect(addRes.status()).toBe(201);
    const cart = await addRes.json();
    expect(cart.items.length).toBeGreaterThanOrEqual(1);
    expect(cart.items[0].product.id).toBe(productId);
  });

  test("logged-in user can add a product to cart", async ({ request }) => {
    const user = makeTestUser();
    const regBody = await registerUser(request, user);
    const token = regBody.token;

    const productsRes = await request.get("/api/products/?type=part");
    const products = await productsRes.json();
    const productId = products[0].id;

    const addRes = await request.post("/api/cart/", {
      headers: authHeaders(token),
      data: { product_id: productId, quantity: 1 },
    });
    expect(addRes.status()).toBe(201);
    const cart = await addRes.json();
    expect(cart.items.length).toBeGreaterThanOrEqual(1);
    expect(cart.items[0].product.id).toBe(productId);
  });

  test("adding same product increments quantity", async ({ request }) => {
    const productsRes = await request.get("/api/products/?type=part");
    const products = await productsRes.json();
    const productId = products[0].id;

    await request.post("/api/cart/", {
      data: { product_id: productId, quantity: 1 },
    });
    const addRes = await request.post("/api/cart/", {
      data: { product_id: productId, quantity: 2 },
    });
    expect(addRes.status()).toBe(200);
    const cart = await addRes.json();
    const item = cart.items.find((i) => i.product.id === productId);
    expect(item.quantity).toBe(3);
  });

  test("can update cart item quantity", async ({ request }) => {
    const productsRes = await request.get("/api/products/?type=part");
    const products = await productsRes.json();
    const productId = products[0].id;

    const addRes = await request.post("/api/cart/", {
      data: { product_id: productId, quantity: 1 },
    });
    const cart = await addRes.json();
    const itemId = cart.items[0].id;

    const patchRes = await request.patch("/api/cart/items/" + itemId + "/", {
      data: { quantity: 5 },
    });
    expect(patchRes.status()).toBe(200);
    const updated = await patchRes.json();
    const item = updated.items.find((i) => i.id === itemId);
    expect(item.quantity).toBe(5);
  });

  test("can remove a cart item", async ({ request }) => {
    const productsRes = await request.get("/api/products/?type=part");
    const products = await productsRes.json();
    const productId = products[0].id;

    const addRes = await request.post("/api/cart/", {
      data: { product_id: productId, quantity: 1 },
    });
    const cart = await addRes.json();
    const itemId = cart.items[0].id;

    const deleteRes = await request.delete("/api/cart/items/" + itemId + "/");
    expect(deleteRes.status()).toBe(200);
    const updated = await deleteRes.json();
    expect(updated.items.find((i) => i.id === itemId)).toBeUndefined();
  });
});

// ─── Cart UI tests ──────────────────────────────────────────────────────────

test.describe("Cart UI", () => {
  test("can add a part to cart from Parts page", async ({ page, request }) => {
    const user = makeTestUser();
    const regBody = await registerUser(request, user);
    const token = regBody.token;

    // Set auth state in the browser
    await page.goto("/");
    await page.evaluate(({ token, userObj }) => {
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(userObj));
    }, { token, userObj: regBody.user });

    // Reload to trigger AuthContext — wait for it
    await page.reload();
    await expect(page.locator(".btn-signout")).toContainText("Sign Out");

    // Go to Parts page
    await page.goto("/parts");
    await expect(page.locator("h1")).toHaveText("Parts & Replacement Batteries");

    // Set up dialog handler before clicking
    page.on("dialog", (dialog) => dialog.accept());

    // Click the first "Add to Cart" button
    const addButton = page.locator("button", { hasText: "Add to Cart" }).first();
    await addButton.click();

    // Navigate to cart to verify item is there
    await page.goto("/cart");
    await expect(page.locator("h1")).toHaveText("Your Cart");
    await expect(page.locator(".cart-item")).toBeVisible();
  });

  test("can view cart and remove item", async ({ page, request }) => {
    const user = makeTestUser();
    const regBody = await registerUser(request, user);
    const token = regBody.token;

    // Seed cart via API
    const productsRes = await request.get("/api/products/?type=part");
    const products = await productsRes.json();
    const productId = products[0].id;
    await request.post("/api/cart/", {
      headers: authHeaders(token),
      data: { product_id: productId, quantity: 1 },
    });

    // Set auth state in browser
    await page.goto("/");
    await page.evaluate(({ token, userObj }) => {
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(userObj));
    }, { token, userObj: regBody.user });
    await page.reload();

    // Wait for auth to resolve before navigating
    await expect(page.locator(".btn-signout")).toContainText("Sign Out");

    // Go to Cart page
    await page.goto("/cart");
    await expect(page.locator("h1")).toHaveText("Your Cart");

    // Should see the item — wait for it to load
    await expect(page.locator(".cart-item")).toContainText(products[0].name);

    // Remove it
    await page.locator("button", { hasText: /remove/i }).first().click();
    await expect(page.locator("text=/empty/i")).toBeVisible();
  });
});