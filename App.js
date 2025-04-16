import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import IntroPage from './pages/IntroPage';
import IndexPage from './pages/indexpage';
import ReviewPage from './pages/reviewpage';
import LoginEmailPage from './pages/LoginEmailPage';
import LoginGithubPage from './pages/LoginGithubPage';
import LoginGooglePage from './pages/LoginGooglePage';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<IntroPage />} />
        <Route path="/index" element={<IndexPage />} />
        <Route path="/review" element={<ReviewPage />} />

        <Route path="/login-email" element={<LoginEmailPage />} />
        <Route path="/login-github" element={<LoginGithubPage />} />
        <Route path="/login-google" element={<LoginGooglePage />} />
      </Routes>
    </Router>
  );
}

export default App;
