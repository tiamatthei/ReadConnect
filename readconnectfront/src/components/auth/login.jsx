import React from "react"; // Import React
import { useNavigate } from "react-router-dom";

const Login = ({ onLoginSuccess }) => {
  const [loginEmail, setLoginEmail] = React.useState(""); // Declare new state variable for login email
  const [loginPassword, setLoginPassword] = React.useState(""); // Declare new state variable for login password
  const [isLoading, setIsLoading] = React.useState(false); // Declare new state variable for loading status
  const [isLoggedIn, setIsLoggedIn] = React.useState(false); // Declare new state variable for login status

  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoading(true); // Update isLoading state when the form is submitted
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        // Send the login email and password to the server
        email: loginEmail,
        password: loginPassword,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Set isLoggedIn to true and isLoading to false
          setIsLoading(false);
          setIsLoggedIn(true);
          onLoginSuccess(data.user);
          //set the user in the local storage
          localStorage.setItem("user", JSON.stringify(data.user));
          //redirect to the home page

          navigate("/");

          console.log(data);
        }
      })
      .catch((error) => {
        console.error(error);
        // Handle the error here
        setIsLoading(false); // Set isLoading to false
      });
  };

  return (
    <div className="login">
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleLogin}>
        <label>
          Correo Electrónico:
          <input
            type="text"
            value={loginEmail}
            onChange={(e) => setLoginEmail(e.target.value)}
          />
        </label>
        <label>
          Contraseña:
          <input
            type="password"
            value={loginPassword}
            onChange={(e) => setLoginPassword(e.target.value)}
          />
        </label>
        {isLoading ? (
          <div className="loading-indicator"></div>
        ) : (
          <button type="submit">Login</button>
        )}{" "}
      </form>
    </div>
  );
};

export default Login; // Export the module
