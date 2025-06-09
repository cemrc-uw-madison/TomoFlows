import React, {useState} from "react";
import { useNavigate, Link } from "react-router-dom";
import { Helmet } from "react-helmet";
import api from '../api.js';
import Cookies from "js-cookie";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import "./Register.css"

/**
 * Register component that allows the user to create an account with their
 * email, password1 and password2 and redirect them to the homepage on success
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Register = (props) => {
	// Initialize state variables and hooks
	const [email, setEmail] = useState("")				// email input state
	const [firstname, setFirstname] = useState("")		// firstname input state
	const [lastname, setLastname] = useState("")		// lastname input state
	const [password1, setPassword1] = useState("")		// password input state
	const [password2, setPassword2] = useState("")		// confirm password state
	const [error, setError] = useState("")				// error response state
	const [loading, setLoading] = useState(false)		// request loading state
	const navigate = useNavigate();						// navigation hook
	
	/**
	 * Calls the API with given email and password to create the user and
	 * return the JSON Web Token (JWT) for the user and store it as a cookie,
	 * and navigate to home page upon success
	 * @returns null
	 */
	const register = () => {
		setLoading(true);
		setError("");
		api.post('/auth/register/', {
			first_name: firstname,
			last_name: lastname,
			email: email,
			password1: password1,
			password2: password2
		})
		.then(response => {
			Cookies.set('auth-token', response.data.access_token)
			Cookies.set('auth-user', JSON.stringify(response.data.user))
			setEmail("");
			setFirstname("");
			setLastname("");
			setPassword1("");
			setPassword2("");
			setLoading(false);
			navigate("/")
		})
		.catch(error => {
			console.error(error);
			if (error.response.status == 400) {
				if ("non_field_errors" in error.response.data) {
					setError(error.response.data.non_field_errors[0]);
				} else if ("email" in error.response.data) {
					setError(error.response.data.email[0]);
					setEmail("");
				} else if ("password1" in error.response.data) {
					setError(error.response.data.password1[0]);
				} else if ("password2" in error.response.data) {
					setError(error.response.data.password2[0]);
				} else {
					setError("Something went wrong! Please try again later.");
				}
			} else if (error.response.status == 401) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setPassword1("");
			setPassword2("");
			setLoading(false);
		});
	}
	
	return (
		<div className="Register">
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
				Create an account
			</p>
			<div className="register-form">
				<Form.Control value={firstname} onChange={e => setFirstname(e.target.value)} placeholder="Enter first name" />
				<Form.Control value={lastname} onChange={e => setLastname(e.target.value)} placeholder="Enter last name" />
				<Form.Control value={email} onChange={e => setEmail(e.target.value)} placeholder="Enter email" />
				<Form.Control value={password1} onChange={e => setPassword1(e.target.value)} type="password" placeholder="Enter password" />
				<Form.Control value={password2} onChange={e => setPassword2(e.target.value)} type="password" placeholder="Confirm password" onKeyDown={(e) => e.key === 'Enter' && register()}/>
				<Button disabled={loading || email.length == 0 || password1.length == 0 || password2.length == 0} onClick={register} variant="light">
					{loading ?
					<Spinner
						as="span"
						animation="border"
						size="sm"
						role="status"
						aria-hidden="true"
					/> :
					"Register"}
				</Button>
			</div>
			<p><small>Already have an account? <Link to={"/login"}>Log in</Link></small></p>
			{error.length != 0 ? 
				<Alert variant="danger" onClose={() => setError("")} dismissible>
					{error}
				</Alert>
				: null
			}
		</div>
	);
};

export default Register;
