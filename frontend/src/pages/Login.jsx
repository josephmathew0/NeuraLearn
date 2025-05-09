// File: frontend/src/pages/Login.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const loginWithGoogle = () => window.location.href = `${import.meta.env.VITE_API_URL}/login/google`;
  const loginWithGithub = () => window.location.href = `${import.meta.env.VITE_API_URL}/login/github`;

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleLogin = async (e) => {
    e.preventDefault();
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    if (data.success) {
      localStorage.setItem("username", data.username);
      localStorage.setItem("email", form.email);
      navigate("/playground");
    } else {
      setError(data.message || "Login failed");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">🔐 Login to NeuraLearn</h2>

        <form onSubmit={handleLogin} className="login-form">
          <input
            name="email"
            placeholder="📧 Email"
            type="email"
            onChange={handleChange}
            required
          />
          <input
            name="password"
            placeholder="🔒 Password"
            type="password"
            onChange={handleChange}
            required
          />
          {error && <p className="error-text">{error}</p>}
          <button type="submit" className="login-btn">Login</button>
        </form>

        <div className="divider">or login with</div>

        <div className="oauth-buttons">
          <button onClick={loginWithGoogle} className="google-btn">Google</button>
          <button onClick={loginWithGithub} className="github-btn">GitHub</button>
        </div>

        <p className="register-link" onClick={() => navigate("/register")}>
          Don't have an account? <span>Register</span>
        </p>
      </div>
    </div>
  );
};

export default Login;
