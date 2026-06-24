import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function SignInPage() {
  const navigate = useNavigate();
  const { isLoggedIn, login, register } = useAuth();
  const [mode, setMode] = useState("login"); // "login" or "register"
  const [form, setForm] = useState({ email: "", password: "", first_name: "", last_name: "" });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  // Already logged in — redirect home
  if (isLoggedIn) {
    navigate("/");
    return null;
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      if (mode === "login") {
        await login(form.email, form.password);
      } else {
        await register(form.email, form.password, form.first_name, form.last_name);
      }
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h1>{mode === "login" ? "Sign In" : "Create Account"}</h1>
      {error && <p className="auth-error" style={{ color: "red" }}>{error}</p>}
      <form className="auth-form" onSubmit={handleSubmit}>
        {mode === "register" && (
          <>
            <div className="form-group">
              <label>First Name</label>
              <input type="text" name="first_name" value={form.first_name} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Last Name</label>
              <input type="text" name="last_name" value={form.last_name} onChange={handleChange} />
            </div>
          </>
        )}
        <div className="form-group">
          <label>Email</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" name="password" value={form.password} onChange={handleChange} required />
        </div>
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? "Please wait..." : mode === "login" ? "Sign In" : "Register"}
        </button>
      </form>
      <p style={{ textAlign: "center", marginTop: "1rem" }}>
        {mode === "login" ? (
          <>Don't have an account? <button onClick={() => setMode("register")} style={{ background: "none", border: "none", color: "var(--accent)", cursor: "pointer", textDecoration: "underline" }}>Register</button></>
        ) : (
          <>Already have an account? <button onClick={() => setMode("login")} style={{ background: "none", border: "none", color: "var(--accent)", cursor: "pointer", textDecoration: "underline" }}>Sign In</button></>
        )}
      </p>
    </div>
  );
}