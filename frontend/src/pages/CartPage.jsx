import React from "react";
import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext.jsx";

export default function CartPage() {
  const { cart, updateQuantity, removeItem } = useCart();

  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <div>
        <h1>Your Cart</h1>
        <p>Your cart is empty.</p>
        <Link to="/ebikes" className="btn btn-primary" style={{ marginTop: "1rem" }}>Browse E-Bikes</Link>
      </div>
    );
  }

  const totalCents = cart.items.reduce((sum, item) => sum + (item.line_total_cents || 0), 0);

  return (
    <div>
      <h1>Your Cart</h1>
      <ul className="cart-list" style={{ marginTop: "1.5rem" }}>
        {cart.items.map((item) => (
          <li className="cart-item" key={item.id}>
            <img src={item.product?.image_url || "https://placehold.co/80x80/eee/1a1a1a?text=Item"} alt={item.product?.name} />
            <div className="cart-item-info">
              <strong>{item.product?.name}</strong>
              {item.variant && <span> ({item.variant.option_name}: {item.variant.option_value})</span>}
              <p>${((item.line_total_cents || 0) / 100).toFixed(2)}</p>
            </div>
            <div className="cart-item-qty">
              <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
              <span>{item.quantity}</span>
              <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
            </div>
            <button className="btn btn-danger" onClick={() => removeItem(item.id)}>Remove</button>
          </li>
        ))}
      </ul>

      <div className="cart-summary">
        <p className="total">Total: ${(totalCents / 100).toFixed(2)}</p>
        <Link to="/checkout" className="btn btn-primary">Checkout</Link>
      </div>
    </div>
  );
}