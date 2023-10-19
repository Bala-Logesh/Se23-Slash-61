import { createContext, useState } from "react";

export const DataContext = createContext();

export const DataContextProvider = ({ children }) => {
  const [productData, setProductData] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <DataContext.Provider value={{ productData, setProductData, searchTerm, setSearchTerm }}>
      {children}
    </DataContext.Provider>
  );
};
