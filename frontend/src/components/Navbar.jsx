import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css'; // Import the CSS for the navbar

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <h1>GroqSense</h1>
      </div>
    <ul>
      <li><Link to="/">Dashboard</Link></li>
      <li><Link to="/screener">Screener</Link></li>
      <li><Link to="/patterns">Pattern Recognition</Link></li>
      <li><Link to="/assistant">AI Assistant</Link></li>
    </ul>
  </nav>
);
};

export default Navbar;
