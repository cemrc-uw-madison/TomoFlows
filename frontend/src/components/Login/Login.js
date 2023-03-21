import React, {useState, useEffect} from "react";
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
	
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			navigate("/");
		}
	}, [])
	
	const login = () => {
		axios.post('/api/auth/login/', {
			email: email,
			password: password
		})
		.then(response => {
			Cookies.set('auth-token', response.data.access_token)
			Cookies.set('refresh-token', response.data.refresh_token)
			setEmail("");
			setPassword("");
			navigate("/")
		})
		.catch(error => {
			console.log(error);
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
