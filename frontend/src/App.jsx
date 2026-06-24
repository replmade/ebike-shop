import React, { useState, useEffect } from "react";
import { Routes, Route, Link, NavLink } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import EbikesPage from "./pages/EbikesPage.jsx";
import EbikeDetailPage from "./pages/EbikeDetailPage.jsx";
import PartsPage from "./pages/PartsPage.jsx";
import AccessoriesPage from "./pages/AccessoriesPage.jsx";
import CartPage from "./pages/CartPage.jsx";
import CheckoutPage from "./pages/CheckoutPage.jsx";
import SignInPage from "./pages/SignInPage.jsx";
import { CartProvider } from "./context/CartContext.jsx";

export default function App() {
  return (
    <CartProvider>
      <div className="app">
        <nav className="navbar">
          <Link to="/" className="logo">VoltCycle</Link>
          <div className="nav-links">
            <NavLink to="/ebikes" className="nav-link">E-Bikes</NavLink>
            <NavLink to="/parts" className="nav-link">Parts</NavLink>
            <NavLink to="/accessories" className="nav-link">Accessories</NavLink>
            <NavLink to="/cart" className="nav-link cart-link">Cart</NavLink>
            <NavLink to="/signin" className="nav-link">Sign In</NavLink>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/ebikes" element={<EbikesPage />} />
            <Route path="/ebikes/:slug" element={<EbikeDetailPage />} />
            <Route path="/parts" element={<PartsPage />} />
            <Route path="/accessories" element={<AccessoriesPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/signin" element={<SignInPage />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>VoltCycle — Fictional ebike shop for demo purposes.</p>
        </footer>
      </div>
    </CartProvider>
  );
}