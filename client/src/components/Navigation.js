import React, { useContext, useEffect } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { AuthContext, defaultUserState } from "../context/AuthContext";

import "../styles/navigation.css";

/**
 * Template for constructing the navigational drawer and appbar
 * @returns
 */
export default function Navigation() {
  const navigate = useNavigate();

  const {
    userData: { isLoggedIn, username },
    setUserData,
  } = useContext(AuthContext);

  useEffect(() => {}, [isLoggedIn]);

  const logout = () => {
    setUserData(defaultUserState);

    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="nav-right">
        <Link to="/" className="title">
          Slash
        </Link>

        {isLoggedIn && (
          <NavLink
            to={"/trends"}
            className={({ isActive }) =>
              isActive ? "navlink activenavlink" : "navlink"
            }
          >
            Trends
          </NavLink>
        )}
        {isLoggedIn && (
          <NavLink
            to={"/tracking"}
            className={({ isActive }) =>
              isActive ? "navlink activenavlink" : "navlink"
            }
          >
            Tracking
          </NavLink>
        )}
      </div>
      <div className="nav-left">
        {!isLoggedIn && (
          <NavLink
            to={"/login"}
            className={({ isActive }) =>
              isActive ? "navlink activenavlink" : "navlink"
            }
          >
            Login
          </NavLink>
        )}
        {!isLoggedIn && (
          <NavLink
            to={"/register"}
            className={({ isActive }) =>
              isActive ? "navlink activenavlink" : "navlink"
            }
          >
            Sign Up
          </NavLink>
        )}
        {isLoggedIn && (
          <p className="navlink" style={{ cursor: "default" }}>
            Hello, {username}
          </p>
        )}
        {isLoggedIn && (
          <NavLink to={""} onClick={logout} className="navlink">
            Log Out
          </NavLink>
        )}
      </div>
    </nav>
  );
}