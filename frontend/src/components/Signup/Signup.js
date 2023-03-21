import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Cookies from "js-cookie";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import "./Signup.css"

const Signup = (props) => {
	const [email, setEmail] = useState("")
	const [password1, setPassword1] = useState("")
	const [password2, setPassword2] = useState("")
	const navigate = useNavigate();
	
	const signup = () => {
		axios.post('/api/auth/signup/', {
			email: email,
			password1: password1,
			password2: password2
		})
		.then(response => {
			Cookies.set('auth-token', response.data.access_token)
			Cookies.set('refresh-token', response.data.refresh_token)
			setEmail("");
			setPassword1("");
			setPassword2("");
			navigate("/")
		})
		.catch(error => {
			console.log(error);
			setPassword1("");
			setPassword2("");
		});
	}
	
	return (
		<div className="Signup">
			<h1>TomoFlows</h1>
			<h5>Sign Up</h5>
			<div className="signup-form">
				<Form.Control value={email} onChange={e => setEmail(e.target.value)} placeholder="Enter email" />
				<Form.Control value={password1} onChange={e => setPassword1(e.target.value)} type="password" placeholder="Enter password" />
				<Form.Control value={password2} onChange={e => setPassword2(e.target.value)} type="password" placeholder="Confirm password" />
				<Button onClick={signup}variant="primary">Sign Up</Button>
			</div>
		</div>
	);
};

export default Signup;
