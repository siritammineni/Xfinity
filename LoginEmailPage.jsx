import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const LoginEmailPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (email && password) {
      setLoginSuccess(true);

      setTimeout(() => {
        navigate('/index');
      }, 2000); // delay to show success message
    } else {
      alert("Please enter both email and password");
    }
  };

  return (
    <div className="login-container">
      <h2>📧 Login with Email</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Enter your Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br />
        <input
          type="password"
          placeholder="Enter your Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br />
        <button type="submit">Login</button>
      </form>

      {loginSuccess && (
        <p className="success-message">✅ You have logged in successfully!</p>
      )}
    </div>
  );
};

export default LoginEmailPage;