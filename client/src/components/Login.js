import React, { useContext, useEffect, useState } from "react";
import Card from "./Card";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { axiosPost } from "../utils/axios";
import { putIntoLocalStorage } from "../utils/helper";

function Login() {
  const navigate = useNavigate();

  const {
    userData: { isLoggedIn },
    setUserData
  } = useContext(AuthContext);

  useEffect(() => {
    if (isLoggedIn) {
      navigate("/");
    }
  }, [isLoggedIn, navigate]);

  let [msg, setMsg] = useState("");

  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    let { password, email } = formData;
    if (email === "" || password === "") {
      setMsg("Please fill in all the fields");
      return;
    }

    const url = "http://localhost:8000/login";
    const data = await axiosPost(url, formData);

    if (data !== undefined) {
      // login successful, you can redirect to the home page
      setUserData({
        isLoggedIn: true,
        user_id: data.user_id,
        email: data.email,
        username: data.username
      });

      putIntoLocalStorage(data);

      setMsg("");
      setFormData({
        email: "",
        password: ""
      });
    } else {
      setMsg("Incorrect credentials");
    }
  };

  return (
    <Card>
      <p className="form-header">Hello there!</p>
      <br />
      {!isLoggedIn && msg === "" && <p className="placeholder">Placeholder for messages</p>}
      {isLoggedIn && msg === "" && <p className="success">Log In successful!</p>}
      {msg !== "" && !isLoggedIn && <p className="error">{msg}</p>}
      <br />
      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        />
        <br />
        <button type="submit">Log In</button>
      </form>

      <div className="form-footer">
        {/* <Link className="link" to="/">
          Forgot Password
        </Link>
        <p className="divider"></p> */}
        <Link className="link" to="/register">
          New here, sign up
        </Link>
      </div>
    </Card>
  );
}

export default Login;
