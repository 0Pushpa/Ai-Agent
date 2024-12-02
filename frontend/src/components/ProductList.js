import React from "react";
import ProductCard from "./ProductCard";
import { CircularProgress, Grid, Typography } from "@mui/material";

function ProductList({ products, loading }) {
  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
        <CircularProgress />
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <Typography variant="h6" style={{ textAlign: "center", marginTop: "20px" }}>
        No products found. Try searching for something else.
      </Typography>
    );
  }

  return (
    <Grid container spacing={3} style={{ padding: "20px" }}>
      {products.map((product) => (
        <Grid item xs={12} sm={6} md={4} key={product.id}>
          <ProductCard product={product} />
        </Grid>
      ))}
    </Grid>
  );
}

export default ProductList;