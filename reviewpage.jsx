import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Document, Packer, Paragraph, TextRun } from 'docx';
import { saveAs } from 'file-saver';
import '../App.css';

const ReviewPage = () => {
  const navigate = useNavigate();
  const [githubURL, setGithubURL] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);

  useEffect(() => {
    const githubURLStored = sessionStorage.getItem('githubURL') || '';
    const uploaded = sessionStorage.getItem('uploadedFiles');
    setGithubURL(githubURLStored);
    setUploadedFiles(uploaded ? JSON.parse(uploaded) : []);
  }, []);

  const toggleSidebar = () => {
    const sidebar = document.getElementById("sidebar");
    if (sidebar.style.left === "0px") {
      sidebar.style.left = "-250px";
    } else {
      sidebar.style.left = "0px";
    }
  };

  const downloadReviewReport = () => {
    alert("Downloading simulated review report... (This would generate a .docx)");
  };

  const generateDocxReport = async () => {
    const doc = new Document({
      sections: [
        {
          properties: {},
          children: [
            new Paragraph({
              children: [
                new TextRun({ text: "VeriCODE - AI Code Review Report", bold: true, size: 28 }),
                new TextRun("\n\nGenerated AI Review Summary:\n"),
                new TextRun("- No critical issues detected.\n"),
                new TextRun("- Optimization suggestions: None available.\n"),
                new TextRun("- Documentation generated: No documentation found.\n"),
                new TextRun("- Final Refactored Code: Available in Review Section.\n"),
                new TextRun("\nThank you for using VeriCODE! 🚀"),
              ],
            }),
          ],
        },
      ],
    });
  
    const blob = await Packer.toBlob(doc);
    saveAs(blob, "VeriCODE_Review_Report.docx");
  };
  
  
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
        <button onClick={() => navigate('/')}>🚪 Logout</button>
      </div>

      <header>
        <h1>Code Review Results</h1>
      </header>

      <main className="review-container">
        <section className="section">
          <h2>📊 Quality Analysis</h2>
          <ul>
            <li>No issues detected.</li>
          </ul>
        </section>

        <section className="section">
          <h2>🪲 Bug Detection</h2>
          <ul>
            <li>No issues detected.</li>
          </ul>
        </section>

        <section className="section">
          <h2>🚀 Optimization Suggestions</h2>
          <ul>
            <li>No optimizations available.</li>
          </ul>
        </section>

        <section className="section">
          <h2>🔧 Final Updated Code (Reframed Code)</h2>
          <p>No documentation generated.</p>
        </section>

        <section className="section">
          <h2>📄 Auto-Generated Documentation</h2>
          <ul>
            <li>No suggestions available.</li>
          </ul>
        </section>

        <section className="section">
          <h2>📝 Summary</h2>
          <ul>
            <li>No suggestions available.</li>
          </ul>
        </section>

        <section className="section">
          <h2>✅ Conclusion</h2>
          <ul>
            <li>No suggestions available.</li>
          </ul>
        </section>

        <button className="download-button" onClick={generateDocxReport}>⬇️ Download Report</button>
        <button className="back-button" onClick={() => navigate('/')}>Back to Home</button>
      </main>
    </div>
  );
};

export default ReviewPage;

