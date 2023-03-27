import React, {useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import "./Projects.css"
import Project from "../../components/Project/Project";

/**
 * Projects component that shows the user their dashboard with relevant features
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Projects = (props) => {
	// Initialize state variables and hooks
	const navigate = useNavigate();					// navigation hook
	
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			axios.get('/api/protected', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => console.log(response))
			.catch(error => {
				console.error(error);
				if (error.response.status === 401 || error.response.status === 403) {
					Cookies.remove('auth-token');
					navigate("/login");
				}
			})
		} else {
			Cookies.remove('auth-token');
			navigate("/login");
		}
	}, [])
	
	return (
		<div className="Projects">
			<Container>
				<h2 className="heading"><b>Projects</b></h2>
				<div className="cards">
					<Project title="Project 1" lastUpdate="2 days" description="Tomography of Protein in XXX"/>
					<Project title="Project 2" lastUpdate="1 week" description="Tomography of Protein in XXX"/>
					<Project title="Project 3" lastUpdate="3 weeks" description="Tomography of Protein in XXX"/>
					<Project createProject />
				</div>
			</Container>
		</div>
	);
};

export default Projects;
