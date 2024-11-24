import React from 'react';

function Contact() {
  return (
    <div className="container mt-5 text-center">
      <img
        src="front-end/src/assets/images/muselogo.png"
        alt="Muse Logo"
        style={{ height: '100px', marginBottom: '20px' }}
      />
      <h1>Contact Us</h1>
      <p>If you have any questions, feel free to reach out!</p>
      <ul className="list-unstyled">
        <li>
          <strong>Email:</strong> <a href="mailto:support@example.com">support@example.com</a>
        </li>
        <li>
          <strong>Phone:</strong> +1 (123) 456-7890
        </li>
        <li>
          <strong>Address:</strong> 123 Main Street, City, State, ZIP
        </li>
      </ul>
    </div>
  );
}

export default Contact;
