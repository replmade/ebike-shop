import React from "react";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div>
      <section className="hero">
        <h1>Ride Further. Ride Electric.</h1>
        <p>Premium electric bikes for commuting, cargo, and trail.</p>
        <Link to="/ebikes" className="hero-cta">Shop E-Bikes</Link>
      </section>

      <div className="category-grid">
        <Link to="/ebikes" className="category-card">
          <img src="https://placehold.co/400x300/1a1a1a/e8b923?text=E-Bikes" alt="E-Bikes" />
          <h3>E-Bikes</h3>
          <p>Three models for every riding style.</p>
        </Link>
        <Link to="/parts" className="category-card">
          <img src="https://placehold.co/400x300/1a1a1a/e8b923?text=Parts" alt="Parts" />
          <h3>Parts</h3>
          <p>Replacement batteries, motors, and components.</p>
        </Link>
        <Link to="/accessories" className="category-card">
          <img src="https://placehold.co/400x300/1a1a1a/e8b923?text=Accessories" alt="Accessories" />
          <h3>Accessories</h3>
          <p>Helmets, locks, racks, and more.</p>
        </Link>
      </div>
    </div>
  );
}