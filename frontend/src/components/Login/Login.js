import React, {useState, } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Cookies from "js-cookie";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import "./Login.css"

const Login = (props) => {
	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")
	const navigate = useNavigate();
	
	const login = () => {
		axios.post('/api/auth/login/', {
			email: email,
			password: password
		})
		.then(res => {
			Cookies.set('auth-token', res.data.access_token)
			Cookies.set('refresh-token', res.data.refresh_token)
			setEmail("");
			setPassword("");
			navigate("/")
		})
		.catch(err => {
			console.log(err);
			setPassword("");
		});
	}
	
	return (
		<div className="Login">
			<h1>TomoFlows</h1>
			<h5>Login</h5>
			<div className="login-form">
				<Form.Control
					value={email}
					onChange={e => setEmail(e.target.value)}
					placeholder="Enter email" 
				/>
				<Form.Control
					value={password}
					onChange={e => setPassword(e.target.value)}
					type="password"
					placeholder="Enter password" 
				/>
				<Button onClick={login} variant="primary">Login</Button>
			</div>
			
		</div>
	);
};

export default Login;
