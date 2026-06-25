import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client.js";
import { useCart } from "../context/CartContext.jsx";

export default function EbikeDetailPage() {
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [adding, setAdding] = useState(false);
  const { addToCart } = useCart();

  useEffect(() => {
    api.getProduct(slug)
      .then(setProduct)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [slug]);

  const handleAddToCart = async () => {
    setAdding(true);
    try {
      await addToCart(product.slug, 1, null);
      alert("Added to cart!");
    } catch (e) {
      alert("Failed to add to cart: " + e.message);
    } finally {
      setAdding(false);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!product) return <p>Product not found.</p>;

  const spec = product.ebike_spec;

  return (
    <div>
      <Link to="/ebikes" className="nav-link">← Back to E-Bikes</Link>
      <div className="product-detail" style={{ marginTop: "1.5rem" }}>
        <div>
          <img src={product.image_url || "/images/voltrider-commuter.jpg"} alt={product.name} />
        </div>
        <div>
          <h1>{product.name}</h1>
          <p className="price" style={{ fontSize: "1.5rem", margin: "0.5rem 0" }}>${product.price}</p>
          <p>{product.description}</p>

          {spec && (
            <table className="spec-table">
              <tbody>
                <tr><th>Motor</th><td>{spec.motor_watts}W</td></tr>
                <tr><th>Battery</th><td>{spec.battery_wh}Wh</td></tr>
                <tr><th>Range</th><td>{spec.range_miles} miles</td></tr>
                <tr><th>Top Speed</th><td>{spec.top_speed_mph} mph</td></tr>
                <tr><th>Frame</th><td>{spec.frame_type}</td></tr>
                <tr><th>Weight</th><td>{spec.weight_lbs} lbs</td></tr>
                <tr><th>Colors</th><td>{(spec.color_options || []).join(", ")}</td></tr>
              </tbody>
            </table>
          )}

          <button className="btn btn-primary" style={{ marginTop: "1.5rem" }} onClick={handleAddToCart} disabled={adding}>
            {adding ? "Adding..." : "Add to Cart"}
          </button>
        </div>
      </div>
    </div>
  );
}