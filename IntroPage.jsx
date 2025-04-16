import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import facebookIcon from '../assets/icons/footer1.png';
import twitterIcon from '../assets/icons/footer2.png';
import linkedinIcon from '../assets/icons/footer3.png'
import '../App.css';

const IntroPage = () => {
  const navigate = useNavigate();
  const [loginModalOpen, setLoginModalOpen] = useState(false);

  return ( 
    
    <div>
      <div className="intro-header">
        <img src="/images/logo1.png" alt="Logo" className="logo" />
        <span className="logo-text">VeriCODE</span>
      </div>

      <div className="top-right-nav">
        <button onClick={() => setLoginModalOpen(true)}>🔐 Login</button>
      </div>

      {loginModalOpen && (
      <div className="modal-overlay" onClick={() => setLoginModalOpen(false)}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <h3>Login Options</h3>
          <button className="modal-btn" onClick={() => navigate('/login-email')}>📧 Login with Email</button>
          <button className="modal-btn" onClick={() => navigate('/login-google')}>🔐 Login with Google</button>
          <button className="modal-btn" onClick={() => navigate('/login-github')}>🐱 Login with GitHub</button>
          <button className="modal-close" onClick={() => setLoginModalOpen(false)}>Close</button>
        </div>
      </div>
      )}

      <div className="intro-container">
        <h1 className="fade-in">
          Empowering Developers with AI-Powered Intelligence{' '}
          <span style={{ color: '#007bff', fontWeight: 600 }}>Code Reviewer.</span>
        </h1>
        <p className="fade-in">Analyze your code for bugs and get documentation with AI.</p>
        <button className="start-btn" onClick={() => navigate('/index')}>
          Start Code Review
        </button>

        <section className="feature-section">
          <div className="card-container">
            <div className="feature-card">
              <h3>🔍 Bug Detection</h3>
              <p>Automatically detect bugs and issues across your codebase using AI models.</p>
            </div>
            <div className="feature-card">
              <h3>🚀 Optimization</h3>
              <p>Get performance improvement suggestions and cleaner code refactoring.</p>
            </div>
            <div className="feature-card">
              <h3>📄 Documentation</h3>
              <p>Generate clear, concise, and structured documentation for your project automatically.</p>
            </div>
          </div>
        </section>
      </div>

      <footer className="footer">
        <div className="footer-section">
          <h3>About VeriCode</h3>
          <p>AI-powered code analysis platform.</p>
        </div>

        <div className="footer-section">
          <h3>Quick Links</h3>
            <Link to ="/">Home</Link><br />
            <a href="contact">Contact</a><br />
            <a href="Features">Features</a>
        </div>

        <div className="footer-section">
          <h3>Follow Us</h3>
          <div className="footer-social-icons">
            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-facebook-f"></i>
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-twitter"></i>
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-linkedin-in"></i>
            </a>
          </div>
        </div>

 
        <div className="footer-bottom">
          © 2025 VeriCode. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default IntroPage;
