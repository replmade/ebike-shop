import React, { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useCart } from "../context/CartContext.jsx";

export default function AccessoriesPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addToCart } = useCart();

  useEffect(() => {
    api.getProducts("accessory")
      .then(setProducts)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const handleAdd = async (productId) => {
    try {
      await addToCart(productId, 1, null);
      alert("Added to cart!");
    } catch (e) {
      alert("Failed: " + e.message);
    }
  };

  if (loading) return <p>Loading accessories...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Accessories</h1>
      <div className="product-grid" style={{ marginTop: "1.5rem" }}>
        {products.map((product) => (
          <div className="product-card" key={product.id}>
            <img src={product.image_url || "/images/helmet.jpg"} alt={product.name} />
            <span className="product-type-badge">{product.product_type}</span>
            <h3>{product.name}</h3>
            <p className="price">${product.price}</p>
            <p>{product.description}</p>
            <button className="btn btn-primary" style={{ marginTop: "0.5rem" }} onClick={() => handleAdd(product.id)}>
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}