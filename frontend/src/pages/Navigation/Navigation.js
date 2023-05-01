import React, { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import "./Navigation.css";

/**
 * Navigation component that provides the user the ability to navigate between
 * the different parts of the application and provides an outlet to the current
 * page that they are on
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Navigation = (props) => {
	const [name, setName] = useState("Loading...");		// name of user state
	const location = useLocation();						// location hook
	const navigate = useNavigate();						// navigation hook
	
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			axios.get('/api/protected', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => {
				let user = JSON.parse(Cookies.get('auth-user'))
				setName(user.first_name + " " + user.last_name)
			})
			.catch(error => {
				if (error.response.status === 401 || error.response.status === 403) {
					Cookies.remove('auth-token');
					Cookies.remove('auth-user');
					navigate("/login");
				}
				console.error(error);
			})
		} else {
			Cookies.remove('auth-token');
			Cookies.remove('auth-user');
			navigate("/login");
		}
	}, [])

	return (
		<div className="Navigation">
			<Navbar collapseOnSelect expand="sm" variant="dark">
				<Container>
					<Navbar.Brand href="/"><b>TomoFlows</b></Navbar.Brand>
					<Navbar.Toggle aria-controls="collapse-nav" />
        			<Navbar.Collapse id="collapse-nav">
						<Nav className="me-auto">
							<Nav.Link href="/" active={location.pathname == "/"}>Projects</Nav.Link>
							<Nav.Link href="/tasks" active={location.pathname == "/tasks"}>Tasks</Nav.Link>
							{/* <Nav.Link href="" active={location.pathname == "/support"}>Support</Nav.Link> */}
						</Nav>
					</Navbar.Collapse>
					<Navbar.Collapse className="justify-content-end">
						<DropdownButton
							title={name}
							align="end"
							variant="outline-light"
							size="sm"
						>
							<Dropdown.Item href="/profile">Profile</Dropdown.Item>
							<Dropdown.Item href="/logout">Logout</Dropdown.Item>
						</DropdownButton>
					</Navbar.Collapse>
				</Container>
			</Navbar>
			<Outlet />
		</div>
	)
}

export default Navigation;
