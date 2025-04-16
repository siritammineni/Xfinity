/*import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginGithubPage = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const CLIENT_ID = 'your_github_client_id';

  const loginWithGithub = () => {
    window.location.assign(`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&scope=user`);
  };

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    const userData = query.get('user');
    if (userData) {
      setUser(JSON.parse(decodeURIComponent(userData)));
      setTimeout(() => {
        navigate('/index');
      }, 2000);
    }
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '100px' }}>
      {user ? (
        <div>
          <h2>👋 Welcome, {user.name || user.login}</h2>
          <p>You have logged in successfully with GitHub</p>
        </div>
      ) : (
        <div>
          <h2>Login with GitHub</h2>
          <button onClick={loginWithGithub}>🐱 Continue with GitHub</button>
        </div>
      )}
    </div>
  );
};

export default LoginGithubPage;*/
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const LoginGithubPage = () => {
  const [showAccounts, setShowAccounts] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const fakeGithubAccounts = [
    { username: 'octocat', email: 'octocat@github.com' },
    { username: 'devhub', email: 'devhub@github.com' },
    { username: 'codezilla', email: 'codezilla@github.com' }
  ];

  const handleGithubLoginClick = () => {
    setShowAccounts(true);
  };

  const handleAccountSelect = (account) => {
    setSuccess(true);
    setTimeout(() => {
      navigate('/index');
    }, 2000);
  };

  return (
    <div className="github-login-page">
      <div className="github-login-box">
        <h2>🐱 Sign in with GitHub</h2>

        {!showAccounts && !success && (
          <button className="github-button" onClick={handleGithubLoginClick}>
            Continue with GitHub
          </button>
        )}

        {showAccounts && !success && (
          <div className="account-list">
            <p>Select a GitHub account:</p>
            {fakeGithubAccounts.map((acc, index) => (
              <button
                key={index}
                className="account-btn"
                onClick={() => handleAccountSelect(acc)}
              >
                {acc.username} ({acc.email})
              </button>
            ))}
          </div>
        )}

        {success && <p className="success-text">✅ You have logged in successfully!</p>}
      </div>
    </div>
  );
};

export default LoginGithubPage;


