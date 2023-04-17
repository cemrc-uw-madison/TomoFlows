import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import ProjectCard from "../../components/ProjectCard/ProjectCard";
import "./Projects.css"

/**
 * Projects component that shows the user their dashboard with relevant features
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Projects = (props) => {
	const [projects, setProjects] = useState([]);
	const [loading, setLoading] = useState(false);
	const [createLoad, setCreateLoad] = useState(false);
	const [show, setShow] = useState(false);
	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");
	const navigate = useNavigate();
	
	useEffect(() => {
		fetchProjects();
	}, [])
	
	const fetchProjects = () => {
		let token = Cookies.get('auth-token')
		if (token) {
			setLoading(true);
			axios.get('/api/projects', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => {
				let data = [...response.data]
				data.sort((a, b) => new Date(b["last_updated"]) - new Date(a["last_updated"]))
				setProjects(data);
				setLoading(false);
			})
			.catch(error => {
				setLoading(false);
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
	}
	
	const handleClose = () => {
		setShow(false);
		setName("");
		setDescription("");
		setCreateLoad(false);
		setError("");
		setSuccess("");
		fetchProjects();
	}
	
	const createProject = () => {
		let token = Cookies.get('auth-token')
		setCreateLoad(true);
		setError("");
		axios.post('/api/projects', 
		{
			name: name,
			description: description
		}, 
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			console.log(response)
			setSuccess(`Project '${name}' created successfully!`)
			setName("");
			setDescription("");
			setCreateLoad(false);
		})
		.catch(error => {
			console.log(error);
			if (error.response.status == 400 || error.response.status == 401) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setName("");
			setDescription("");
			setCreateLoad(false)
		});
	}
	
	return (
		<div className="Projects">
			<Container>
				<h2 className="heading"><b>Projects</b></h2>
				<div className="cards">
				{loading ? 
					<Spinner animation="border" variant="primary" /> :
					<>
						{
							projects.map((project, idx) => 
								<ProjectCard
									key={project.id}
									id={project.id}
									name={project.name}
									description={project.description}
									lastUpdated={project.last_updated}
								/>
							)
						}
						<ProjectCard createProject toggle={() => setShow(true)} />
					</>
				}
				</div>
			</Container>
			<Modal centered show={show} onHide={handleClose}>
				<Modal.Header>
					<Modal.Title>Create Project</Modal.Title>
				</Modal.Header>
				<Modal.Body className="create-project">
					<Form.Control
						disabled={createLoad}
						value={name}
						onChange={e => setName(e.target.value)}
						placeholder="Project Name" 
					/>
					<Form.Control
						disabled={createLoad}
						value={description}
						onChange={e => setDescription(e.target.value)}
						placeholder="Project Description" 
					/>
					{error.length != 0 && 
						<Alert variant="danger" onClose={() => setError("")} dismissible>
							{error}
						</Alert>
					}
					{success.length != 0 &&
						<Alert variant="success" onClose={() => setSuccess("")} dismissible>
							{success}
						</Alert>
					}
				</Modal.Body>
				<Modal.Footer>
					<Button variant="secondary" onClick={handleClose}>
						Cancel
					</Button>
					<Button
						className="create-project-button"
						variant="primary"
						onClick={createProject}
						disabled={name.length == 0 || description.length == 0}
					>
						{
							createLoad ?
							<Spinner
								as="span"
								animation="border"
								size="sm"
								role="status"
								aria-hidden="true"
							/> :
							"Create"
						}
					</Button>
				</Modal.Footer>
			</Modal>
		</div>
	);
};

export default Projects;
