import React from "react";
import ReactDOM from "react-dom/client";
import {
	createBrowserRouter,
	RouterProvider,
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
import CreateAccount from "./pages/CreateAccount/CreateAccount";
import ResetPassword from "./pages/ResetPassword/ResetPassword";

/* React-Router-Dom Routing Configuration */
const router = createBrowserRouter([
	{
		path: "/",
		element: <Navigation />,
		errorElement: <Error />,
		children: [
			{
			  path: "",
			  element: <Projects />,
			},
			{
				path: "/profile",
				element: <Profile />,
			},
			{
				path: "project/:id",
				element: <Project />,
			},
			{
				path: "tasks",
				element: <Tasks />,
			},
			{
				path: "create-account",
				element: <CreateAccount/>
			},
			{
				path: "reset-password",
				element: <ResetPassword/>
			}
		]
	},
	{
		path: "/login",
		element: <Login />,
		errorElement: <Error />
	},
	{
		path: "/logout",
		element: <Logout />,
		errorElement: <Error />
	},
	{
		path: "/register",
		element: <Register />,
		errorElement: <Error />
	},
]);

/* Inject RouterProvider component to the HTML */
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<Toaster/>
		<RouterProvider router={router} />
	</React.StrictMode>
);
