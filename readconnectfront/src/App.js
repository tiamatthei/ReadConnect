import React, { useState } from 'react';
import './App.css'; // Import the CSS file

function App() {
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  const [registrationUsername, setRegistrationUsername] = useState('');
  const [registrationPassword, setRegistrationPassword] = useState('');
  const [registrationEmail, setRegistrationEmail] = useState('');
  const [registrationSuccess, setRegistrationSuccess] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: loginUsername,
        password: loginPassword
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Handle the response data here
    })
    .catch(error => {
      console.error(error);
      // Handle the error here
    });
  };

  const handleRegister = (e) => {
    e.preventDefault();
    fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: registrationUsername,
        password: registrationPassword,
        email: registrationEmail
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setRegistrationSuccess(true);
      // Handle the response data here
    })
    .catch(error => {
      console.error(error);
      // Handle the error here
    });
  };

  return (
    <div className="container"> {/* Add a class name to the container */}
      {registrationSuccess && <p>Registration successful! Please login.</p>}
      <div className="login">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <label>
            Nombre de Usuario:
            <input type="text" value={loginUsername} onChange={(e) => setLoginUsername(e.target.value)} />
          </label>
          <label>
            Contraseña:
            <input type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} />
          </label>
          <button type="submit">Login</button>
        </form>
      </div>

      <div className="register">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <label>
            Nombre de Usuario:
            <input type="text" value={registrationUsername} onChange={(e) => setRegistrationUsername(e.target.value)} />
          </label>
          <label>
            Contraseña:
            <input type="password" value={registrationPassword} onChange={(e) => setRegistrationPassword(e.target.value)} />
          </label>
          <label>
            Email:
            <input type="email" value={registrationEmail} onChange={(e) => setRegistrationEmail(e.target.value)} />
          </label>
          <button type="submit">Register</button>
        </form>
      </div>
    </div>
  );
}

export default App;
