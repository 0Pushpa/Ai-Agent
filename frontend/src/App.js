import React, { useState,useEffect } from "react";
import axios from "axios";
import SearchBar from "./components/SearchBar";
import ProductList from "./components/ProductList";
import Recommendations from "./components/Recommendations";

function App() {
  const [products, setProducts] = useState([]);
  const [recommendations, setRecommendations] = useState(""); // State for AI recommendations
  const [query, setQuery] = useState("");
  useEffect(() => {
    console.log("Search Response:", products);
  }, [products]);
  
  const handleSearch = async () => {
    try {
      const response = await axios.get("http://localhost:8000/search", {
        params: { query },
      });
      setProducts(response.data.products);
      setRecommendations(response.data.recommendations); // Set recommendations from backend
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1 style={{ textAlign: "center", color: "#1976d2" }}>
        Product Price Tracker with Recommendations
      </h1>
      <SearchBar
        query={query}
        setQuery={setQuery}
        onSearch={handleSearch}
      />
      <div style={{ marginTop: "20px" }}>
        <ProductList products={products} />
      </div>
      {recommendations && (
        <div style={{ marginTop: "20px" }}>
          <Recommendations text={recommendations} />
        </div>
      )}
    </div>
  );
}

export default App;
