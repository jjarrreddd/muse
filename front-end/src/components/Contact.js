import React from 'react';
import logo from './images/muselogo.png'
import { motion } from 'framer-motion';
import './style.css';

function Contact() {
  return (
    <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1 }}>
      <div className="body-center mt-5 text-center">
        <h1 className="header">Contact Us</h1>
        <p className="body">If you have any questions, feel free to reach out!</p>
        <ul className="list-unstyled">
          <li>
            <strong>Email:</strong> <a href="mailto:jarredethen@gmail.com">jarredethen@gmail.com</a>
          </li>
          <li>
            <strong>Phone:</strong> +1 (123) 456-7890
          </li>
        </ul>
        <br />
        <ul className="list-unstyled">
          <li>
            <strong>Email:</strong> <a href="mailto:support@example.com">support@example.com</a>
          </li>
          <li>
            <strong>Phone:</strong> +1 (123) 456-7890
          </li>
        </ul>
        <br />
        <ul className="list-unstyled">
          <li>
            <strong>Email:</strong> <a href="mailto:support@example.com">support@example.com</a>
          </li>
          <li>
            <strong>Phone:</strong> +1 (123) 456-7890
          </li>
        </ul>
        <br />
        <img
          src={logo}
          alt="Muse Logo"
          style={{ height: '100px', marginBottom: '20px' }}
        />
      </div>
      </motion.div>
  );
}

export default Contact;