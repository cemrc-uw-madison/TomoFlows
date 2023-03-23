import React from "react";
import ReactDOM from "react-dom/client";
import {
	createBrowserRouter,
	RouterProvider,
} from "react-router-dom";
import "./index.css";
import Home from "./components/Home/Home";
import Error from "./components/Error/Error";
import Login from "./components/Login/Login";
import Logout from "./components/Logout/Logout";
import Register from "./components/Register/Register";

/* React-Router-Dom Routing Configuration */
const router = createBrowserRouter([
	{
		path: "/",
		element: <Home />,
		errorElement: <Error />
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
		<RouterProvider router={router} />
	</React.StrictMode>
);
