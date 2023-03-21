import React, { useEffect, useMemo } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Cookies from 'js-cookie';
import "./Logout.css"

const useQuery = () => {
	const { search } = useLocation();
	return useMemo(() => new URLSearchParams(search), [search]);
}

const Logout = (props) => {
	let query = useQuery();
	const navigate = useNavigate();
	
	useEffect(() => {
		if (query.get("click") === "1") {
			logout()
		}
	}, [])
	
	const logout = () => {
		axios.post('/api/auth/logout/')
		.then(res => {
			Cookies.remove('auth-token');
			Cookies.remove('refresh-token');
			navigate("/");
		})
		.catch(err => {
			console.log(err);
			setPassword("");
		});
	}
	
	return (
		<div className="Logout">
			<h1>TomoFlows</h1>
			<h5>Logout</h5>
			<Button onClick={logout} variant="primary">Logout</Button>
		</div>
	);
};

export default Logout;
