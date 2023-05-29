import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet";
import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';
import Cookies from 'js-cookie';
import "./Logout.css"

/**
 * Logout component immediately logs out the current logged in user
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Logout = (props) => {
	const navigate = useNavigate();
	
	useEffect(() => {
		setTimeout(logout, 1500)
	}, [])
	
	/**
	 * Calls the API with the given JSON Web Token (JWT)
	 * to log out the user and disable to token for use until next login
	 * @returns null
	 */
	const logout = () => {
		axios.post('/api/auth/logout/')
		.then(response => {
			Cookies.remove('auth-token');
			Cookies.remove('auth-user');
			navigate("/");
		})
		.catch(error => {
			console.log(error);
			Cookies.remove('auth-token');
			Cookies.remove('auth-user');
			navigate("/");
		});
	}
	
	return (
		<div className="Logout">
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
				Logging you out...
			</p>
			<Spinner animation="border" variant="light" />
		</div>
	);
};

export default Logout;
