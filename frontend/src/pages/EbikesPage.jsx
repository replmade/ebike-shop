import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";

export default function EbikesPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.getProducts("ebike")
      .then(setProducts)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading e-bikes...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Electric Bikes</h1>
      <div className="product-grid" style={{ marginTop: "1.5rem" }}>
        {products.map((product) => (
          <Link to={`/ebikes/${product.slug}`} key={product.id} className="product-card">
            <img src={product.image_url || "https://placehold.co/400x300/eee/1a1a1a?text=Ebike"} alt={product.name} />
            <h3>{product.name}</h3>
            <p className="price">${product.price}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}