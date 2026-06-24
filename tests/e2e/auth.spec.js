import { test, expect } from "@playwright/test";

/**
 * Generate a unique test user for each test to avoid collisions.
 */
function makeTestUser() {
  const id = Date.now() + Math.random().toString(36).slice(2, 6);
  return {
    email: `test_${id}@example.com`,
    password: "TestPass123!",
    firstName: "Test",
    lastName: "User",
  };
}

/**
 * Register a user via API and return credentials + response body.
 */
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

/**
 * Log in via API and return the response body (token + user).
 */
async function loginUser(request, user) {
  const response = await request.post("/api/auth/login/", {
    data: { email: user.email, password: user.password },
  });
  expect(response.status()).toBe(200);
  return response.json();
}

test.describe("Authentication API", () => {
  test("can register a new user", async ({ request }) => {
    const user = makeTestUser();
    const body = await registerUser(request, user);
    expect(body.token).toBeDefined();
    expect(body.user.email).toBe(user.email);
  });

  test("cannot register with missing fields", async ({ request }) => {
    const response = await request.post("/api/auth/register/", {
      data: { email: "" },
    });
    expect(response.status()).toBe(400);
  });

  test("cannot register duplicate email", async ({ request }) => {
    const user = makeTestUser();
    await registerUser(request, user);

    const response = await request.post("/api/auth/register/", {
      data: {
        email: user.email,
        password: user.password,
        first_name: user.firstName,
        last_name: user.lastName,
      },
    });
    expect(response.status()).toBe(400);
  });

  test("can log in with valid credentials", async ({ request }) => {
    const user = makeTestUser();
    await registerUser(request, user);
    const body = await loginUser(request, user);
    expect(body.token).toBeDefined();
    expect(body.user.email).toBe(user.email);
  });

  test("cannot log in with wrong password", async ({ request }) => {
    const user = makeTestUser();
    await registerUser(request, user);

    const response = await request.post("/api/auth/login/", {
      data: { email: user.email, password: "WrongPassword!" },
    });
    expect(response.status()).toBe(401);
  });

  test("cannot log in with missing fields", async ({ request }) => {
    const response = await request.post("/api/auth/login/", {
      data: {},
    });
    expect(response.status()).toBe(400);
  });

  test("cannot log in with nonexistent email", async ({ request }) => {
    const response = await request.post("/api/auth/login/", {
      data: { email: "nobody@example.com", password: "Whatever123!" },
    });
    expect(response.status()).toBe(401);
  });
});

test.describe("Sign-in UI", () => {
  test("sign-in page shows login form", async ({ page }) => {
    await page.goto("/signin");
    await expect(page.locator("h1")).toHaveText("Sign In");
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
  });

  test("can toggle to register form", async ({ page }) => {
    await page.goto("/signin");
    await page.locator("button", { hasText: "Register" }).click();
    await expect(page.locator("h1")).toHaveText("Create Account");
    await expect(page.locator('input[name="first_name"]')).toBeVisible();
    await expect(page.locator('input[name="last_name"]')).toBeVisible();
  });

  test("can sign in via UI and see Sign Out in navbar", async ({ page, request }) => {
    const user = makeTestUser();
    await registerUser(request, user);

    await page.goto("/signin");
    await page.locator('input[name="email"]').fill(user.email);
    await page.locator('input[name="password"]').fill(user.password);
    await page.locator('button[type="submit"]').click();

    // Should redirect to home
    await expect(page).toHaveURL(/\//);

    // Navbar should show Sign Out with the user's email
    await expect(page.locator(".btn-signout")).toContainText("Sign Out");
    await expect(page.locator(".btn-signout")).toContainText(user.email);
    await expect(page.locator('a.nav-link', { hasText: "Sign In" })).toBeHidden();
  });

  test("can sign out and see Sign In in navbar", async ({ page, request }) => {
    const user = makeTestUser();
    await registerUser(request, user);

    await page.goto("/signin");
    await page.locator('input[name="email"]').fill(user.email);
    await page.locator('input[name="password"]').fill(user.password);
    await page.locator('button[type="submit"]').click();
    await expect(page.locator(".btn-signout")).toBeVisible();

    // Sign out
    await page.locator(".btn-signout").click();

    // Navbar should show Sign In again
    await expect(page.locator('a.nav-link', { hasText: "Sign In" })).toBeVisible();
  });

  test("shows error on invalid credentials", async ({ page }) => {
    await page.goto("/signin");
    await page.locator('input[name="email"]').fill("nobody@example.com");
    await page.locator('input[name="password"]').fill("WrongPass123!");
    await page.locator('button[type="submit"]').click();

    // Wait for the error element to appear (avoid strict-mode violation from generic <p>)
    await expect(page.locator(".auth-error")).toContainText(/invalid|error/i);
  });
});