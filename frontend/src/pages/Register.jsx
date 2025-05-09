import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRegister = async (e) => {
    e.preventDefault();
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    if (data.success) {
      localStorage.setItem("username", form.username);
      localStorage.setItem("email", form.email);
      navigate("/playground");
    } else {
      setError(data.message || "Registration failed");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h2 className="text-xl font-bold mb-4">Create Account</h2>
      <form onSubmit={handleRegister} className="w-full max-w-xs space-y-3">
        <input name="username" placeholder="Username" value={form.username} onChange={handleChange} className="p-2 border w-full" required />
        <input name="email" placeholder="Email" type="email" value={form.email} onChange={handleChange} className="p-2 border w-full" required />
        <input name="password" placeholder="Password" type="password" value={form.password} onChange={handleChange} className="p-2 border w-full" required />
        {error && <p className="text-red-500">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white p-2 w-full rounded">Register</button>
      </form>
    </div>
  );
};

export default Register;
