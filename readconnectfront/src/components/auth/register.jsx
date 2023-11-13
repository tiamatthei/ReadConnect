import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register({ onLoginSuccess }) {
  const [registrationEmail, setRegistrationEmail] = useState("");
  const [registrationUsername, setRegistrationUsername] = useState("");
  const [registrationPassword, setRegistrationPassword] = useState("");
  const [registrationSuccess, setRegistrationSuccess] = useState(false);
  const [isLoading, setIsLoading] = React.useState(false); // Declare new state variable for loading status

  const navigate = useNavigate();
  
  const handleRegister = (e) => {
    setIsLoading(true); // Update isLoading state when the form is submitted
    e.preventDefault();
    fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: registrationUsername,
        password: registrationPassword,
        email: registrationEmail,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.success) {
          setIsLoading(false);
          setRegistrationSuccess(true);
          //refresh the page
          onLoginSuccess(data.user);
          //set the user in the local storage
          localStorage.setItem("user", JSON.stringify(data.user));
          navigate("/");
        }
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false); // Set isLoading to false
      });
  };

  return (
    <div className="register">
      <h2>Registrarse</h2>
      <form onSubmit={handleRegister}>
        <label>
          Nombre de Usuario:
          <input
            type="text"
            value={registrationUsername}
            onChange={(e) => setRegistrationUsername(e.target.value)}
          />
        </label>
        <label>
          Contraseña:
          <input
            type="password"
            value={registrationPassword}
            onChange={(e) => setRegistrationPassword(e.target.value)}
          />
        </label>
        <label>
          Email:
          <input
            type="email"
            value={registrationEmail}
            onChange={(e) => setRegistrationEmail(e.target.value)}
          />
        </label>
        {isLoading ? (
          <div className="loading-indicator"></div>
        ) : (
          <button type="submit">Registro</button>
        )}{" "}
      </form>
      {registrationSuccess && <p>Registration successful!</p>}
    </div>
  );
}

export default Register;
