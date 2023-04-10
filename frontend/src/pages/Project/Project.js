import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { PencilSquare, Trash } from "react-bootstrap-icons"
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from "react-bootstrap/Container";
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from "react-bootstrap/Button";
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import "./Project.css";

const Project = (props) => {
	const { id } = useParams();
	const [project, setProject] = useState({});
	const [loading, setLoading] = useState(true);
	const [editLoad, setEditLoad] = useState(false);
	const [deleteLoad, setDeleteLoad] = useState(false);
	const [show, setShow] = useState(false);
	const [showDelete, setShowDelete] = useState(false);
	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");
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
				setName(response.data.name);
				setDescription(response.data.description)
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
	
	const editProject = () => {
		let token = Cookies.get('auth-token')
		setEditLoad(true);
		setError("");
		axios.put(`/api/projects/${id}`, 
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
			setSuccess(`Project '${name}' updated successfully!`)
			setEditLoad(false);
		})
		.catch(error => {
			console.log(error);
			if (error.response.status == 400 || error.response.status == 401) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setEditLoad(false)
		});
	}
	
	const deleteProject = () => {
		let token = Cookies.get('auth-token')
		setDeleteLoad(true);
		setError("");
		axios.delete(`/api/projects/${id}`,
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			console.log(response)
			setShowDelete(false);
			setDeleteLoad(false);
			navigate("/");
		})
		.catch(error => {
			console.log(error);
			setDeleteLoad(false);
			if (error.response.status in [401, 403, 404]) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
		});
	}
	
	const handleClose = () => {
		setShow(false);
		setEditLoad(false);
		setError("");
		setSuccess("");
		fetchProject();
	}
	
	const handleDeleteClose = () => {
		setShowDelete(false);
		setError("");
		setSuccess("");
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
							<h2><b>{project.name}</b></h2>
							<p className="text-body-secondary">{project.description}</p>
						</div>
						<div className="button-div">
							<Button
								className="primary-button"
								variant="primary"
								onClick={() => setShow(true)}
							>	
								<PencilSquare />
								Edit Project
							</Button>
							<Button
								className="primary-button"
								onClick={() => setShowDelete(true)}
							>	
								<Trash />
								Delete Project
							</Button>
						</div>
					</div>
				</>
			}
			</Container>
			<Modal centered show={show} onHide={handleClose}>
				<Modal.Header>
					<Modal.Title>Edit Project</Modal.Title>
				</Modal.Header>
				<Modal.Body className="edit-project">
					<Form.Control
						disabled={editLoad}
						value={name}
						onChange={e => setName(e.target.value)}
						placeholder="Project Name" 
					/>
					<Form.Control
						disabled={editLoad}
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
						className="edit-project-button"
						variant="primary"
						onClick={editProject}
						disabled={name.length == 0 || description.length == 0}
					>
						{
							editLoad ?
							<Spinner
								as="span"
								animation="border"
								size="sm"
								role="status"
								aria-hidden="true"
							/> :
							"Save"
						}
					</Button>
				</Modal.Footer>
			</Modal>
			<Modal centered show={showDelete} onHide={handleDeleteClose}>
				<Modal.Header>
					<Modal.Title>Delete Project</Modal.Title>
				</Modal.Header>
				<Modal.Body className="edit-project">
					<p>
						Are you sure you want to delete this project? 
					</p>
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
					<Button variant="secondary" onClick={handleDeleteClose}>
						Cancel
					</Button>
					<Button
						className="delete-project-button"
						variant="danger"
						onClick={deleteProject}
					>
						{
							deleteLoad ?
							<Spinner
								as="span"
								animation="border"
								size="sm"
								role="status"
								aria-hidden="true"
							/> :
							"Delete"
						}
					</Button>
				</Modal.Footer>
			</Modal>
		</div>
	)
}

export default Project
