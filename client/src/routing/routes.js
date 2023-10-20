import React from "react";
import Login from "../components/Login";

export const routes = [
  {
    path: "/",
    name: "Home",
    element: <h1>Slash</h1>,
    login: false,
  },
  {
    path: "/login",
    name: "Login",
    element: <Login />,
    login: false,
  },
];


