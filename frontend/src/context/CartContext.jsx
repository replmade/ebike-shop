import React, { createContext, useContext, useState, useCallback, useEffect } from "react";
import { api } from "../api/client.js";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [cart, setCart] = useState(null);
  const [cartCount, setCartCount] = useState(0);

  const refreshCart = useCallback(async () => {
    try {
      const data = await api.getCart();
      setCart(data);
      setCartCount(data.items ? data.items.length : 0);
    } catch {
      // Not logged in or no cart yet — that's fine
    }
  }, []);

  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  const addToCart = useCallback(async (productId, quantity = 1, variantId = null) => {
    const data = await api.addToCart(productId, quantity, variantId);
    setCart(data);
    setCartCount(data.items ? data.items.length : 0);
    return data;
  }, []);

  const updateQuantity = useCallback(async (itemId, quantity) => {
    const data = await api.updateCartItem(itemId, quantity);
    setCart(data);
    setCartCount(data.items ? data.items.length : 0);
    return data;
  }, []);

  const removeItem = useCallback(async (itemId) => {
    const data = await api.removeFromCart(itemId);
    setCart(data);
    setCartCount(data.items ? data.items.length : 0);
    return data;
  }, []);

  return (
    <CartContext.Provider value={{ cart, cartCount, refreshCart, addToCart, updateQuantity, removeItem }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
}