const API_BASE = "/api";

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const token = localStorage.getItem("token");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(error.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Auth
  register: (email, password, firstName = "", lastName = "") =>
    request("/auth/register/", {
      method: "POST",
      body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName }),
    }),

  login: (email, password) =>
    request("/auth/login/", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  // Products
  getProducts: (type = null) => {
    const params = type ? `?type=${type}` : "";
    return request(`/products/${params}`);
  },

  getProduct: (slug) =>
    request(`/products/${slug}/`),

  // Cart
  getCart: () => request("/cart/"),
  addToCart: (productId, quantity = 1, variantId = null) =>
    request("/cart/", {
      method: "POST",
      body: JSON.stringify({ product_id: productId, quantity, variant_id: variantId }),
    }),
  updateCartItem: (itemId, quantity) =>
    request(`/cart/items/${itemId}/`, {
      method: "PATCH",
      body: JSON.stringify({ quantity }),
    }),
  removeFromCart: (itemId) =>
    request(`/cart/items/${itemId}/`, { method: "DELETE" }),

  // Checkout
  checkout: (shippingData) =>
    request("/checkout/", {
      method: "POST",
      body: JSON.stringify(shippingData),
    }),
};