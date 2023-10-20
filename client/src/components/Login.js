import React, { useContext, useEffect, useState } from "react";
import Card from "./Card";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Login() {
    const navigate = useNavigate();

    const {
        userData: { isLoggedIn },
        setUserData,
    } = useContext(AuthContext);

    useEffect(() => {
        if (isLoggedIn) {
            navigate("/");
        }
    }, [isLoggedIn, navigate]);

    let [msg, setMsg] = useState("");

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        let { password, email } = formData;
        if (email === "" || password === "") {
            setMsg("Please fill in all the fields");
            return;
        }

        console.log(formData);
        return;

        // Send login data to the backend API
        try {
        } catch (error) { }
    };

    return (
        <Card>
            <p className="form-header">Hello there!</p>
            <br />
            {!isLoggedIn && msg === "" && (
                <p className="placeholder">Placeholder for messages</p>
            )}
            {isLoggedIn && msg === "" && (
                <p className="success">Log In successful!</p>
            )}
            {msg !== "" && !isLoggedIn && <p className="error">{msg}</p>}
            <br />
            <form onSubmit={handleSubmit} className="form">
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
                    onChange={(e) =>
                        setFormData({ ...formData, password: e.target.value })
                    }
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