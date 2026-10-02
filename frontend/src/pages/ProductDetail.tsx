import { useParams, Link } from "react-router-dom";
import productsData from "../data/products.json";
import type { Product } from "../types";
import "./ProductDetail.css";

const products = productsData as Product[];

function ProductDetail() {
  const { productId } = useParams<{ productId: string }>();
  const product = products.find((p) => p.product_id === productId);

  if (!product) {
    return (
      <div className="page">
        <p>Product not found.</p>
        <Link to="/products">Back to Products</Link>
      </div>
    );
  }

  return (
    <div className="page product-detail" data-product-id={product.product_id}>
      <div className="product-detail-image">
        <img src={`/${product.image_file_path}`} alt={product.name} />
      </div>
      <div className="product-detail-info">
        <h1>{product.name}</h1>
        <p className="product-detail-price">${product.price.toFixed(2)}</p>
        <p className="product-detail-description">{product.description}</p>

        {product.colors.length > 0 && (
          <p className="product-detail-colors">
            <strong>Colors:</strong> {product.colors.join(", ")}
          </p>
        )}

        <h2>Sizes &amp; Availability</h2>
        <ul className="product-detail-sizes">
          {product.sizes.map((s) => (
            <li
              key={s.size}
              className={s.quantity > 0 ? "in-stock" : "out-of-stock"}
            >
              <span className="size-label">{s.size}</span>
              <span className="size-stock">
                {s.quantity > 0 ? `${s.quantity} in stock` : "Out of stock"}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default ProductDetail;
