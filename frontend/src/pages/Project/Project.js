import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Spinner from 'react-bootstrap/Spinner';
import "./Project.css";

const Project = (props) => {
	const { id } = useParams();
	const [project, setProject] = useState({});
	const [loading, setLoading] = useState(true);
	const navigate = useNavigate();
	
	useEffect(() => {
		fetchProject();
	}, [])
	
	const fetchProject = () => {
		let token = Cookies.get('auth-token')
		if (token) {
			setLoading(true);
			axios.get(`/api/projects/${id}`, {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => {
				setProject(response.data);
				setLoading(false);
			})
			.catch(error => {
				setLoading(false);
				if (error.response.status === 401 || error.response.status === 403 || error.response.status === 404) {
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
	}
	return (
		<div className="Project">
			<Container>
			{loading ? 
				<div className="div">
					<Spinner animation="border" variant="primary" />
				</div> :
				<>	
					<div className="heading">
						<div>
							<h3>{project.name}</h3>
							<p className="text-body-secondary">{project.description}</p>
						</div>
						<div className="button-div">
							<Button
								variant="outline-primary"
							>	
								Run
							</Button>
							<Button
								variant="outline-primary"
							>
								Run
							</Button>
						</div>
					</div>
				</>
			}
			</Container>
		</div>
	)
}

export default Project
