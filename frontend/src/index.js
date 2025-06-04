import React from "react";
import ReactDOM from "react-dom/client";
import { 
	HashRouter, 
	Routes, 
	Route, 
} from "react-router-dom";
import { Toaster } from 'react-hot-toast';
import "./index.css";
import Error from "./pages/Error/Error";
import Navigation from "./pages/Navigation/Navigation";
import Login from "./pages/Login/Login";
import Logout from "./pages/Logout/Logout";
import Register from "./pages/Register/Register";
import Projects from "./pages/Projects/Projects";
import Project from "./pages/Project/Project";
import Tasks from "./pages/Tasks/Tasks";
import Profile from "./pages/Profile/Profile";

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <HashRouter>
    <Routes>
      <Route path="/" element={<Navigation />} errorElement={<Error />}>
        <Route index element={<Projects />} />
        <Route path="profile" element={<Profile />} />
        <Route path="project/:id" element={<Project />} />
        <Route path="tasks" element={<Tasks />} />
      </Route>
      <Route path="login" element={<Login />} />
      <Route path="logout" element={<Logout />} />
      <Route path="register" element={<Register />} />
    </Routes>
  </HashRouter>
);
