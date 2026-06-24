import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client.js";

export default function CheckoutPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    shipping_name: "",
    shipping_addr1: "",
    shipping_addr2: "",
    shipping_city: "",
    shipping_state: "",
    shipping_zip: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [order, setOrder] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await api.checkout(form);
      setOrder(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (order) {
    return (
      <div>
        <h1>Order Confirmed!</h1>
        <p>Thank you for your purchase.</p>
        <p>Order ID: {order.id}</p>
        <p>Total: ${order.total}</p>
        <button className="btn btn-primary" style={{ marginTop: "1rem" }} onClick={() => navigate("/")}>
          Continue Shopping
        </button>
      </div>
    );
  }

  return (
    <div>
      <h1>Checkout</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form className="checkout-form" style={{ marginTop: "1.5rem" }} onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name</label>
          <input type="text" name="shipping_name" value={form.shipping_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Address Line 1</label>
          <input type="text" name="shipping_addr1" value={form.shipping_addr1} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Address Line 2 (optional)</label>
          <input type="text" name="shipping_addr2" value={form.shipping_addr2} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>City</label>
          <input type="text" name="shipping_city" value={form.shipping_city} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>State</label>
          <input type="text" name="shipping_state" value={form.shipping_state} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>ZIP Code</label>
          <input type="text" name="shipping_zip" value={form.shipping_zip} onChange={handleChange} required />
        </div>
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? "Placing Order..." : "Place Order"}
        </button>
      </form>
    </div>
  );
}