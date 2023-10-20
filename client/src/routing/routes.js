import React from "react";
import Login from "../components/Login";
import Search from "../components/Search";

export const routes = [
  {
    path: "/",
    name: "Home",
    element: <Search />,
    login: false,
  },
  {
    path: "/login",
    name: "Login",
    element: <Login />,
    login: false,
  },
];


