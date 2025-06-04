import React, {useState, useEffect} from "react";
import { useNavigate, Link } from "react-router-dom";
import { Helmet } from "react-helmet";
import axios from 'axios';
import api from '../api.js';
import Cookies from "js-cookie";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import "./Login.css"

/**
 * Login component that allows the user to authenticate with their 
 * email and password and redirect them to the homepage on success
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Login = (props) => {
	// Initialize state variables and hooks
	const [email, setEmail] = useState("")				// email input state
	const [password, setPassword] = useState("")		// password input state
	const [loading, setLoading] = useState(false)		// request loading state
	const [error, setError] = useState("")				// error response state
	const navigate = useNavigate();						// navigation hook
	
	/* hook to navigate to home if already authenticated */
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			navigate("/");
		}
	}, [])
	
	/**
	 * Calls the API with given email and password to return the JSON Web Token (JWT)
	 * for the user and store it as a cookie, and navigate to home page upon success
	 * @returns null
	 */
	const login = () => {
		setLoading(true);
		setError("");
		/* axios.post('/api/auth/login/', { */
		api.post('/auth/login', {
			email: email,
			password: password
		})
		.then(response => {
			Cookies.set('auth-token', response.data.access_token)
			Cookies.set('auth-user', JSON.stringify(response.data.user))
			setEmail("");
			setPassword("");
			setLoading(false);
			navigate("/");
		})
		.catch(error => {
			console.error(error);
			if (error.response.status == 400) {
				if ("non_field_errors" in error.response.data) {
					setError(error.response.data.non_field_errors[0]);
				} else if ("email" in error.response.data) {
					setError(error.response.data.email[0]);
					setEmail("");
				} else if ("password" in error.response.data) {
					setError(error.response.data.password[0]);
				}
				else {
					setError("Something went wrong! Please try again later.");
				}
			} else if (error.response.status == 401) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setPassword("");
			setLoading(false)
		});
	}
	
	return (
		<div className="Login">
			<Helmet>
				<html data-bs-theme="dark" lang="en" amp />
                <style type="text/css">{`
					body {
						background-color: #38023B;
					}
				`}</style>
            </Helmet>
			<h1><b>TomoFlows</b></h1>
			<p className="lead">
				Log in to your account
			</p>
			<div className="login-form">
				<Form.Control
					value={email}
					onChange={e => setEmail(e.target.value)}
					placeholder="Enter email" 
				/>
				<Form.Control
					value={password}
					onChange={e => setPassword(e.target.value)}
					onKeyDown={(e) => {
						if (e.key === 'Enter' && !loading && email.length != 0 && password.length != 0)
							login();
					}}
					type="password"
					placeholder="Enter password" 
				/>
				<Button disabled={loading || email.length == 0 || password.length == 0} onClick={login} variant="light">
					{
						loading ?
						<Spinner
							as="span"
							animation="border"
							size="sm"
							role="status"
							aria-hidden="true"
					  	/> :
						"Login"
					}
				</Button>
			</div>
			{/* <p><small><Link to={"/register"}>Forgot Password</Link></small></p> */}
			<p><small>Don't have an account? <Link to={"/register"}>Register</Link></small></p>
			{error.length != 0 ? 
				<Alert variant="danger" onClose={() => setError("")} dismissible>
					{error}
				</Alert>
				: null
			}
		</div>
	);
};

export default Login;
