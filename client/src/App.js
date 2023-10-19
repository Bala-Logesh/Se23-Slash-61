import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import Routing from "./routing/Routing";
import { AuthContextProvider } from "./context/AuthContext";
import { DataContextProvider } from "./context/DataContext";

/**
 * Main point of rendering for the interactive web page
 * @returns
 */
function App() {
  return (
    <div className="container">
      <AuthContextProvider>
        <DataContextProvider>
          <Router>
            <Routing />
          </Router>
        </DataContextProvider>
      </AuthContextProvider>
    </div>
  );
}

export default App;
