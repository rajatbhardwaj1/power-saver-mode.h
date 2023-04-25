import React from 'react';
import { FaSearch, FaUser } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import './navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <FaUser className="navbar-icon" />
        <h3 className="navbar-brand">My App</h3>
      </div>
      <div className="navbar-middle">
        <input type="text" className="navbar-search" placeholder="Search..." />
        <button className="navbar-search-button">
          <FaSearch className="navbar-search-icon" />
        </button>
      </div>
      <div className="navbar-right">
        <Link to="/chats" className="navbar-link">Chats</Link>
        <Link to="/groups" className="navbar-link">Groups</Link>
        <Link to="/profile" className="navbar-link">Profile</Link>
      </div>
    </nav>
  );
}

export default Navbar;
