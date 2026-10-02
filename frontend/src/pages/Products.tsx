import { Link } from "react-router-dom";
import productsData from "../data/products.json";
import { useChatMatches } from "../context/ChatMatchContext";
import type { Product } from "../types";
import "./Products.css";

const products = productsData as Product[];

function orderByMatches(items: Product[], matchedIds: string[]): Product[] {
  if (matchedIds.length === 0) return items;

  const matchedSet = new Set(matchedIds);
  const matched = items.filter((p) => matchedSet.has(p.product_id));
  const unmatched = items.filter((p) => !matchedSet.has(p.product_id));
  return [...matched, ...unmatched];
}

function Products() {
  const { matchedProductIds } = useChatMatches();
  const orderedProducts = orderByMatches(products, matchedProductIds);
  const matchedSet = new Set(matchedProductIds);

  return (
    <div className="page page-yale-pattern">
      <h1>Products</h1>
      <div className="product-grid">
        {orderedProducts.map((product) => (
          <Link
            key={product.product_id}
            to={`/products/${product.product_id}`}
            className={
              matchedSet.has(product.product_id)
                ? "product-card chat-match"
                : "product-card"
            }
          >
            <img
              src={`/${product.image_file_path}`}
              alt={product.name}
              className="product-card-image"
            />
            <div className="product-card-body">
              <h3 className="product-card-name">{product.name}</h3>
              <p className="product-card-description">
                {product.description}
              </p>
              <p className="product-card-price">
                ${product.price.toFixed(2)}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Products;
