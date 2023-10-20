import React from "react";
import Login from "../components/Login";
import Register from "../components/Register";
import Search from "../components/Search";
import Results from "../components/Results";
import IndTracking from "../components/IndTracking";
import Trends from "../components/Trends";

import products from "../data/products";

export const routes = [
  {
    path: "/",
    name: "Home",
    element: <Search />,
    login: false
  },
  {
    path: "/login",
    name: "Login",
    element: <Login />,
    login: false
  },
  {
    path: "/register",
    name: "Register",
    element: <Register />,
    login: false
  },
  {
    path: "/results",
    name: "Result",
    element: <Results products={products} />,
    login: false
  },
  {
    path: "/tracking",
    name: "Tracking",
    element: <Results products={products.filter((product) => product.tracked === true)} />,
    login: true
  },
  {
    path: "/tracking/:id",
    name: "IndTracking",
    element: <IndTracking />,
    login: true
  },
  {
    path: "/Trends",
    name: "trends",
    element: <Trends />,
    login: false
  }
];
