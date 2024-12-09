import React from 'react';
import { Link } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import logo from './images/muselogo.png';

function NavBar() {
  return (
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container">
          <AnimatePresence>
            <Link className="navbar-brand" to="/">
              <img
                src={logo}
                alt="Muse Logo"
                style={{ height: '50px', marginRight: '10px' }}
              />
              Muse
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">
                    Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/about">
                    About
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/contact">
                    Contact
                  </Link>
                
                <li className="nav-item">
                <Link className="nav-link" to="/music-player">
                    Music Player
                </Link>
                </li>
                </li>
              </ul>
            </div>
          </AnimatePresence>
        </div>
      </nav>
  );
}

export default NavBar;