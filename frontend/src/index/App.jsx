import * as React from 'react';
import { useState } from "react";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import NavBar from "/components/NavBar";
import Dashboard from "/components/Dashboard";
import Landing from "/components/Landing";
import SignupForm from "/components/SignupForm";
import SigninForm from "/components/SigninForm";
import * as authService from "../services/authservice";
import Header from "/components/Header";

const App = () => {
  const [user, setUser] = useState(authService.getUser());

  const handleSignout = () => {
    authService.signout();
    setUser(null);
  };

  return (
    <BrowserRouter>
      <Header />
      <NavBar user={user} handleSignout={handleSignout} />
      <Routes>
        {user ? (
          <Route path="/" element={<Dashboard user={user} />} />
        ) : (
          <Route path="/" element={<Landing />} />
        )}
        <Route path="/signup" element={<SignupForm setUser={setUser} />} />
        <Route path="/signin" element={<SigninForm setUser={setUser} />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
