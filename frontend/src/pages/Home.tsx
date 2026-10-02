import { Link } from "react-router-dom";
import productsData from "../data/products.json";
import type { Product } from "../types";
import "./Home.css";

const products = productsData as Product[];

interface CategorySection {
  title: string;
  keyword: string;
}

const SECTIONS: CategorySection[] = [
  { title: "Our Best Hoodies", keyword: "hoodie" },
  { title: "Our Hottest Long Sleeves", keyword: "long-sleeve" },
  { title: "Crewneck Favorites", keyword: "crewneck" },
  { title: "Classic T-Shirts", keyword: "t-shirt" },
];

function productsFor(keyword: string): Product[] {
  return products
    .filter((p) => p.garment_type.toLowerCase().includes(keyword))
    .slice(0, 4);
}

const BULLDOG_BANNER_BEFORE = "Crewneck Favorites";

function Home() {
  return (
    <div className="page page-yale-pattern">
      <img
        src="/yale-students.jpg"
        alt="Yale students welcoming the incoming class"
        className="home-hero-image"
      />
      <h1>Yale Campus Customs</h1>
      <p className="home-intro">Your home for Yale-themed collegiate apparel.</p>

      {SECTIONS.map((section) => {
        const items = productsFor(section.keyword);
        if (items.length === 0) return null;

        return (
          <div key={section.title}>
            {section.title === BULLDOG_BANNER_BEFORE && (
              <div className="home-bulldog-banner">
                <img src="/yale-bulldog.webp" alt="Yale Bulldog" />
                <span className="home-bulldog-caption">Dan's favorites</span>
              </div>
            )}
            <section className="home-section">
              <div className="home-section-header">
                <h2>{section.title}</h2>
                <Link to="/products" className="home-section-link">
                  Shop all products
                </Link>
              </div>
              <div className="home-section-grid">
                {items.map((product) => (
                  <Link
                    key={product.product_id}
                    to={`/products/${product.product_id}`}
                    className="home-product-card"
                  >
                    <img
                      src={`/${product.image_file_path}`}
                      alt={product.name}
                      className="home-product-image"
                    />
                    <div className="home-product-name">{product.name}</div>
                    <div className="home-product-price">
                      ${product.price.toFixed(2)}
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          </div>
        );
      })}
    </div>
  );
}

export default Home;
