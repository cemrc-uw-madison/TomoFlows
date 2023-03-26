import React from "react";
import { Outlet, useLocation } from "react-router-dom";
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
	const location = useLocation();

	return (
		<div className="Navigation">
			<Navbar collapseOnSelect expand="sm" variant="dark">
				<Container>
					<Navbar.Brand href="/"><b>TomoFlows</b></Navbar.Brand>
					<Navbar.Toggle aria-controls="collapse-nav" />
        			<Navbar.Collapse id="collapse-nav">
						<Nav className="me-auto">
							<Nav.Link href="/" active={location.pathname == "/"}>Projects</Nav.Link>
							<Nav.Link href="/pipelines" active={location.pathname == "/pipelines"}>Pipelines</Nav.Link>
							<Nav.Link href="" active={location.pathname == "/support"}>Support</Nav.Link>
						</Nav>
					</Navbar.Collapse>
					<Navbar.Collapse className="justify-content-end">
						<DropdownButton
							title="John Smith" // TODO: Change to currently logged in user
							align="end"
							variant="outline-light"
							size="sm"
						>
							<Dropdown.Item href="">Profile</Dropdown.Item>
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
