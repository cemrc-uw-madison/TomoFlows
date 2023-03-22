import React from "react";
import ReactDOM from "react-dom/client";
import {
	createBrowserRouter,
	RouterProvider,
} from "react-router-dom";
import App from "./components/App/App";
import Error from "./components/Error/Error";
import Login from "./components/Login/Login";
import Logout from "./components/Logout/Logout";
import Signup from "./components/Signup/Signup";

const router = createBrowserRouter([
	{
		path: "/",
		element: <App />,
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
		path: "/signup",
		element: <Signup />,
		errorElement: <Error />
	},
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
);
