import React, { useState } from "react";
import { TextField, Button } from "@mui/material";

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSearchClick = () => {
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", margin: "20px 0" }}>
      <TextField
        label="Search for Products"
        variant="outlined"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "300px", marginRight: "10px" }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSearchClick}
        style={{ height: "56px" }}
      >
        Search
      </Button>
    </div>
  );
}

export default SearchBar;
