import React, { useState } from "react";
import { Route, Switch, Redirect } from "react-router-dom"; // Import Route, and Switch
import './App.css'; // Import the CSS file
import Register from "./Register";

function App() {
  const [registrationSuccess, setRegistrationSuccess] = useState(false);


  return (
    <div className="container"> {/* Add a class name to the container */}
      {registrationSuccess && <p>Registration successful! Please login.</p>}
      <Switch>
        <Route exact path="/">
          <Login />
          <Register setRegistrationSuccess={setRegistrationSuccess} />
        </Route>
        <Route path="/home">
          {isLoggedIn ? <Home /> : <Redirect to="/" />} {/* Conditionally render the Home component */}
        </Route>
      </Switch>
    </div>
  );
}

function Home() {
  return (
    <div>
      <h1>Welcome to the Home Page!</h1>
    </div>
  );
}

export default App;
