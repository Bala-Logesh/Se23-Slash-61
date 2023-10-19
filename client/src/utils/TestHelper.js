import React from "react";
import { AuthContext } from "../context/AuthContext";
import { DataContext } from "../context/DataContext";
import { BrowserRouter } from "react-router-dom";

function TestHelper({ children }) {
  const userData = {
    isLoggedIn: true,
    username: "test",
    email: "test@gmail.com",
    user_id: 0
  };

  const data = {
    productData: [],
    setProductData: () => {
      productData = [];
    },
    searchTerm: "laptop",
    setSearchTerm: () => {
      searchTerm = val;
    }
  };

  return (
    <AuthContext.Provider value={{ userData }}>
      <DataContext.Provider value={{ data }}>
        <BrowserRouter>{children}</BrowserRouter>
      </DataContext.Provider>
    </AuthContext.Provider>
  );
}

export default TestHelper;
