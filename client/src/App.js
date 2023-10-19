import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import Routing from "./routing/Routing";

/**
 * Main point of rendering for the interactive web page
 * @returns
 */
function App() {
  return (
    <div className="container">
      <Router>
        <Routing />
      </Router>
    </div>
  );
}

export default App;
