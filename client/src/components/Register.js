import React, { useContext, useEffect, useState } from "react";
import Card from "./Card";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { axiosPost } from "../utils/axios";

function Register() {
  const navigate = useNavigate();

  const {
    userData: { isLoggedIn }
  } = useContext(AuthContext);

  useEffect(() => {
    if (isLoggedIn) {
      navigate("/");
    }
  }, [isLoggedIn, navigate]);

  let [registered, setRegistered] = useState(false);
  let [msg, setMsg] = useState("");

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confpassword: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    let { username, password, email, confpassword } = formData;
    if (username === "" || email === "" || password === "" || confpassword === "") {
      setMsg("Please fill in all the fields");
      setRegistered(false);
      return;
    }

    if (confpassword !== password) {
      setMsg("Passwords do not match");
      setRegistered(false);
      return;
    }

    const url = "http://localhost:8000/register/";
    const data = await axiosPost(url, formData);
    
    if (data !== undefined) {
      // register successful, you can redirect to the login page
      setRegistered(true);
      setMsg("");

      setFormData({
        email: "",
        password: "",
        confpassword: "",
        username: ""
      });

      setTimeout(() => {
        setMsg("");
        navigate("/login");
      }, 2000);
    } else {
      setRegistered(false);
      setMsg("Registration unsuccessful");
    }
  };

  return (
    <Card>
      <p className="form-header">Hello there!</p>
      <br />
      {!registered && msg === "" && <p className="placeholder">Placeholder for messages</p>}
      {registered && msg === "" && <p className="success">Registration successful!</p>}
      {msg !== "" && !registered && <p className="error">{msg}</p>}
      <br />
      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          placeholder="Username"
          value={formData.username}
          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
        />
        <br />
        <input
          type="email"
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
        <input
          type="password"
          placeholder="Confirm Password"
          value={formData.confpassword}
          onChange={(e) => setFormData({ ...formData, confpassword: e.target.value })}
        />
        <br />
        <button type="submit">Sign Up</button>
      </form>

      <div className="form-footer">
        <Link className="link" to="/login">
          Already registered, log in
        </Link>
      </div>
    </Card>
  );
}

export default Register;
