import React from "react";
import "./App.css";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/auth/login";
import Register from "./components/auth/register";
import Home from "./pages/home";
import Perfil from "./pages/perfil";

function App() {
  const [isLogin, setIsLogin] = React.useState(false);

  function onLoginSuccess() {
    setIsLogin(true);
  }
  //if the session has a user, then the user is logged in
  React.useEffect(() => {
    if (sessionStorage.getItem("user")) {
      setIsLogin(true);
    }
  }, []);

  function handleLogout() {
    setIsLogin(false);
    sessionStorage.removeItem("user");
    // redirect to login page
    return <Navigate to="/login" />;
  }

  return (
    <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              isLogin ? <Navigate to="/home" /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/login"
            element={
              <div className="container">
                <Login onLoginSuccess={onLoginSuccess} />
                <Register />
              </div>
            }
          />
          <Route path="/home" element={<Home handleLogout={handleLogout} />} />
          <Route path="/perfil" element={<Perfil handleLogout={handleLogout}/>} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
