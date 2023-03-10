import React, {useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Cookies from 'js-cookie';
import "./App.css"

const App = (props) => {
	const [res, setRes] = useState()
	const [loggedIn, setLoggedIn] = useState(false)
	const navigate = useNavigate();
	
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			setLoggedIn(true);
			axios.get('/api/protected', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => setRes(response.data.message))
			.catch(error => console.error(error))
		} else {
			fetch("/api/ping")
			.then(response => response.json())
			.then(data => setRes(data.message))
			.catch(error => console.log(error))
		}
	}, [])
	
	return (
		<div className="App">
			<h1>TomoFlows</h1>
			<p><b>API Response {loggedIn ? "(Logged In)": null}: </b> {res ?? "Loading..."}</p>
			{loggedIn  
				? <Button onClick={() => navigate("/logout")} variant="primary">Logout</Button>
				: <Button onClick={() => navigate("/login")} variant="primary">Login</Button>
			}
		</div>
	);
};

export default App;
