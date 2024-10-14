import React, {useState} from "react";
import { useNavigate, Link } from "react-router-dom";
import { Helmet } from "react-helmet";
import axios from 'axios';
import Cookies from "js-cookie";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import "./Register.css"
import toast from 'react-hot-toast';

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
	const [labName, setLabName] = useState("")		// lab name input state
	const [institutionName, setInstitutionName] = useState("")		// institution name state
	const [password1, setPassword1] = useState("");
	const [password2, setPassword2] = useState("");
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
		axios.post('/api/auth/register/', {
			first_name: firstname,
			last_name: lastname,
			email: email,
			password1: password1,
			password2: password2
		})
		.then(response => {
			setLoading(true);
			axios.post('/api/request-account', {
				email: email,
				labName: labName,
				institutionName, institutionName,
			}
			).then(response => {
				setEmail("");
				setFirstname("");
				setLastname("");
				setLabName("");
				setInstitutionName("");
				setPassword1("");
				setPassword2("");
				setLoading(false);
				navigate("/login");
				toast.success('An request has been sent to admin user');
			})
		}).catch(error => {
			if (error.response.status == 400) {
				if ("non_field_errors" in error.response.data) {
					setError(error.response.data.non_field_errors[0]);
				} else if ("email" in error.response.data) {
					setError(error.response.data.email[0]);
					setEmail("");
				} else if ("labName" in error.response.data) {
					setError(error.response.data.labName[0]);
				} else if ("insitutionName" in error.response.data) {
					setError(error.response.data.institutionName[0]);
				} else if ("password1" in error.response.data) {
					setError(error.response.data.password1[0]);
				} else if ("password2" in error.response.data) {
					setError(error.response.data.password2[0]);
				} else else {
					setError("Something went wrong! Please try again later.");
				}
			} else if (error.response.status == 401) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
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
			
			<div className="register-board">
				<div className="register-info">
					<section>
						<h1 className="lead">
							Request an account
						</h1>
						<p>
							Get your TomoFlows account info placeholder 
						</p>
					</section>
				</div>
				<div className="register-form">
						<Form.Control value={firstname} onChange={e => setFirstname(e.target.value)} placeholder="First name" />
						<Form.Control value={lastname} onChange={e => setLastname(e.target.value)} placeholder="Last name" />
						<Form.Control value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
						<Form.Control value={labName} onChange={e => setLabName(e.target.value)} placeholder="Lab Name" />
						<Form.Control value={institutionName} onChange={e => setInstitutionName(e.target.value)} placeholder="Institution Name" />
						<Form.Control value={password1} onChange={e => setPassword1(e.target.value)} placeholder="Password" type="password"/>
						<Form.Control value={password2} onChange={e => setPassword2(e.target.value)} placeholder="Confirm Password" onKeyDown={(e) => e.key === 'Enter' && register()} type="password"/>
						<Button disabled={loading || firstname.length == 0 || lastname.length == 0 || email.length == 0 || labName.length == 0 || institutionName.length == 0} onClick={register} variant="light">
							{loading ?
							<Spinner
								as="span"
								animation="border"
								size="sm"
								role="status"
								aria-hidden="true"
							/> :
							"Request"}
						</Button>
				</div>
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
