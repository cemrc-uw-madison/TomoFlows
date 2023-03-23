import React, {useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Cookies from 'js-cookie';
import "./Home.css"

/**
 * Home component that shows the user their dashboard with relevant features
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Home = (props) => {
	// Initialize state variables and hooks
	const [res, setRes] = useState("")				// API response state
	const navigate = useNavigate();					// navigation hook
	
	/* hook for different actions based on login state */
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			axios.get('/api/protected', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => setRes(response.data.message))
			.catch(error => {
				if (error.response.status === 401) {
					navigate("/logout");
				}
				console.error(error);
			})
		} else {
			navigate("/login");
		}
	}, [])
	
	return (
		<div className="Home">
			<h2>TomoFlows</h2>
			<p><b>API Response (Logged In): </b> {res.length == 0 ? "Loading..." : res}</p>
			<div>
				<Button onClick={() => navigate("/logout")} variant="primary">Logout</Button>
			</div>
		</div>
	);
};

export default Home;
