import React from 'react';
import { Link } from 'react-router-dom';
// import './Navbar.css'; // optional

const Navbar = () => (
  <nav className="navbar">
    <h2>GroqSense</h2>
    <ul>
      <li><Link to="/">Dashboard</Link></li>
      <li><Link to="/screener">Screener</Link></li>
      <li><Link to="/assistant">AI Assistant</Link></li>
    </ul>
  </nav>
);

export default Navbar;
