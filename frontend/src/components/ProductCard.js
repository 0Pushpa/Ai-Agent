import React from "react";
import { Card, CardContent, CardMedia, Typography } from "@mui/material";

function ProductCard({ product }) {
  return (
    <Card style={{ maxWidth: "345px", margin: "auto" }}>
      <CardMedia
        component="img"
        height="200"
        image={product.image || "https://via.placeholder.com/200"}
        alt={product.title}
      />
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {product.title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Price: ${product.price}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Source: {product.source}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default ProductCard;
