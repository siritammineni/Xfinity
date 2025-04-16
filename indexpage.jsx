import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const IndexPage = () => {
  const [githubURL, setGithubURL] = useState('');
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState([]);
  const [repoFiles, setRepoFiles] = useState([]);
  const navigate = useNavigate();

  const handleAnalyze = () => {
    if (!githubURL && files.length === 0) {
      alert("Please provide a GitHub URL or upload files.");
      return;
    }

    setLoading(true);

    // Simulate storing data
    setTimeout(() => {
      sessionStorage.setItem("githubURL", githubURL);
      sessionStorage.setItem("uploadedFiles", JSON.stringify([...files].map(f => f.name)));

      navigate('/review');
    }, 2000);
  };

  const fetchRepoFiles = async () => {
    const cleanURL = githubURL.trim().replace(/\.git$/, '');
  
    const match = cleanURL.match(/^https:\/\/github\.com\/([^\/]+)\/([^\/]+)$/);
    if (!match) {
      alert("Invalid GitHub repository URL.");
      return;
    }
  
    const [_, owner, repo] = match;
  
    const apiURL = `https://api.github.com/repos/${owner}/${repo}/contents`;
  
    try {
      const response = await fetch(apiURL);
      if (!response.ok) throw new Error("GitHub API failed");
  
      const files = await response.json();
      const fileData = files.map(file => ({
        name: file.name,
        url: file.html_url
      }));

      setRepoFiles(fileData); // store for display
  
    } catch (error) {
      console.error("Error fetching repo files:", error.message);
      alert("Failed to fetch files. Make sure the GitHub repo is public.");
    }
  };  

  /*const handleShowFiles = () => {
    if (!githubURL) {
      alert("Please enter a GitHub repository URL.");
      return;
    }
    alert(`Simulated: fetching files from ${githubURL}`);
  };*/

  return (
    <div>
      <div className="intro-header">
        <img src="/images/logo1.png" alt="Logo" className="logo" />
        <span className="logo-text">VeriCODE</span>
      </div>

      <div className="top-right-nav">
      <a href="/">🏠 Home</a>
        <button onClick={() => document.body.classList.toggle('dark-mode')}>
          🌓 Toggle Mode
        </button>
        <a href="https://github.com/" target="_blank" rel="noreferrer">
          🐙 GitHub
        </a>
      </div>

      <main className="container">
        <section className="intro-section">
          <h2>Welcome to AI Code Reviewer</h2>
          <p>Analyze your code with AI-powered insights. Detect issues, optimize performance, and generate documentation effortlessly.</p>
        </section>

        <section className="upload-section">
          <h2>Get Started</h2>
          <div className="input-button-group">
            <input
              type="text"
              placeholder="Enter GitHub Repo URL"
              value={githubURL}
              onChange={(e) => setGithubURL(e.target.value)}
            />
            <button onClick={fetchRepoFiles}>📂 Show Files</button>
          </div>
          
          <input
            type="file"
            id="file-upload"
            multiple
            onChange={(e) => setFiles(e.target.files)}
          />
          <div style={{ margin: '10px 0' }} ></div>
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? '🔄 Analyzing...' : 'Analyze'}
          </button>

          {/* Show uploaded file names */}
          {repoFiles.length > 0 && (
            <div className="file-list-container">
              <h3>📁 Files in Respository</h3>
              <ul>
                {repoFiles.map((file, index) => (
                  <li key={index}>
                    <a href={file.url} target="_blank" rel="noopener noreferrer">
                    {file.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>
      {/*-------------------------------------------------------}
      {/*<main className="index-layout">
        {/* Left GIF section */}
        {/*<div className="gif-section">
          <img src="" alt="Robot AI" className="robot-gif" />
        </div>*/}

        {/* Right Form section */}
        {/*<div className="container">

          <section className="intro-section">
            <h2>Welcome to AI Code Reviewer</h2>
            <p>Analyze your code with AI-powered insights. Detect issues, optimize performance, and generate documentation effortlessly.</p>
          </section>

          <section className="upload-section">
            <h2>Get Started</h2>
            <div className="input-button-group">
              <input
                type="text"
                placeholder="Enter GitHub Repo URL"
                value={githubURL}
                onChange={(e) => setGithubURL(e.target.value)}
              />
              <button onClick={fetchRepoFiles}>📂 Show Files</button>
            </div>

            <input
              type="file"
              id="file-upload"
              multiple
              onChange={(e) => setFiles(e.target.files)}
            />
            <div style={{ margin: '10px 0' }} ></div>
            <button onClick={handleAnalyze} disabled={loading}>
              {loading ? '🔄 Analyzing...' : 'Analyze'}
            </button>

            {repoFiles.length > 0 && (
              <div className="file-list-container">
                <h3>📁 Files in Repository</h3>
                <ul>
                  {repoFiles.map((file, index) => (
                    <li key={index}>
                      <a href={file.url} target="_blank" rel="noopener noreferrer">
                      {file.name}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        </div>
      </main>*/}


    </div>
  );
};

export default IndexPage;

