// src/App.jsx
import React, { useState } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setData(null);

    try {
      // Adjust the URL if your Django backend is running on a different host/port
      const response = await fetch(`http://localhost:8000/api/github/${username}`);
      if (!response.ok) {
        throw new Error("User not found or error fetching data");
      }
      const jsonData = await response.json();
      setData(jsonData);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>GitHub User Data</h1>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Enter GitHub username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <button type="submit">Search</button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      {data && (
        <div className="data-table">
          <h2>User Overview</h2>
          <table>
            <tbody>
              <tr>
                <th>Username</th>
                <td>{data.username}</td>
              </tr>
              <tr>
                <th>Total Commits</th>
                <td>{data.total_commits}</td>
              </tr>
              <tr>
                <th>Total Pull Requests</th>
                <td>{data.total_pull_requests}</td>
              </tr>
              <tr>
                <th>Total Merged Pull Requests</th>
                <td>{data.total_merged_pull_requests}</td>
              </tr>
            </tbody>
          </table>

          <h2>Repositories</h2>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>URL</th>
              </tr>
            </thead>
            <tbody>
              {data.repositories && data.repositories.map((repo) => (
                <tr key={repo.id}>
                  <td>{repo.name}</td>
                  <td>
                    <a href={repo.html_url} target="_blank" rel="noopener noreferrer">
                      {repo.html_url}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
