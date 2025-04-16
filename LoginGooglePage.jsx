import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode} from 'jwt-decode';
import '../App.css';

const LoginGooglePage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleSuccess = (credentialResponse) => {
    const decoded = jwtDecode(credentialResponse.credential);
    console.log("User Info:", decoded);
    setSuccessMessage("You have logged in successfully!");

    setTimeout(() => {
      navigate('/index');
    }, 2000);
  };

  const handleError = () => {
    alert("Google Sign-In failed");
  };

  return (
    <div className="login-container">
      <h2>Login with Google</h2>
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={handleError}
      />
      {successMessage && <p style={{ color: 'green', marginTop: '15px' }}>{successMessage}</p>}
    </div>
  );
};

export default LoginGooglePage;

