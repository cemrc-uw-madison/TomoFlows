import React from "react";
import ReactDOM from "react-dom/client";
import {
	createBrowserRouter,
	RouterProvider,
} from "react-router-dom";
import "./index.css";
import Error from "./pages/Error/Error";
import Navigation from "./pages/Navigation/Navigation";
import Login from "./pages/Login/Login";
import Logout from "./pages/Logout/Logout";
import Register from "./pages/Register/Register";
import Projects from "./pages/Projects/Projects";
import Pipelines from "./pages/Pipelines/Pipelines";

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
				path: "pipelines",
				element: <Pipelines />,
			},
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
		<RouterProvider router={router} />
	</React.StrictMode>
);
