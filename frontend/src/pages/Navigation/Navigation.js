import React, { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { PlusLg, Trash } from "react-bootstrap-icons"
import Cookies from 'js-cookie';
import api from '../api.js';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import "./Navigation.css";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

// Automatically determine base path from current location
export const BASE_PREFIX = getCookie("BASE_PREFIX") || "/";

/**
 * Navigation component that provides the user the ability to navigate between
 * the different parts of the application and provides an outlet to the current
 * page that they are on
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Navigation = (props) => {
	const [name, setName] = useState("Loading...");		// name of user state
	const [show, setShow] = useState(false);			// create modal open state
	const [code, setCode] = useState("");				// verification code input state
	const [taskName, setTaskName] = useState("")		// task name input state
	const [description, setDescription] = useState("")	// task description input state
	const [fields, setFields] = useState([])			// tasks parameter fields input state
	const [loading, setLoading] = useState(false)		// API request loading state
	const [error, setError] = useState("")				// API response error state
	const [success, setSuccess] = useState("")			// API response success state
	const [key, setKey] = useState("r4x")				// outlet key state
	const location = useLocation();						// location hook
	const navigate = useNavigate();						// navigation hook
	
	useEffect(() => {
		let token = Cookies.get('auth-token')
		if (token) {
			api.get('/protected', {
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
	
	/**
	 * function to handle close of the create task modal and reset the 
	 * corresponding state variables
	 */
	const handleClose = () => {
		setKey(Math.random().toString(36).substring(2,7))
		setShow(false);
		setCode("");
		setTaskName("");
		setDescription("");
		setFields([]);
		setLoading(false);
		setError("");
		setSuccess("");
	}
	
	/**
	 * function to handle the submission of the create task form
	 * and send a request to the backend to create the task
	 */
	const createTask = () => {
		let token = Cookies.get('auth-token')
		setError("");
		for (let field of fields) {
			if (field["name"].length === 0) {
				setError("Paramater name is required");
				return;
			}
			if (field["type"].length === 0) {
				setError("Parameter type is required")
				return;
			}
			if (field["type"] !== "file" && field["default"].length === 0) {
				setError("Parameter default value is required")
				return;
			}
		}
		setLoading(true);
		api.post('tasks', {
			verification_code: code,
			name: taskName,
			description: description,
			parameter_fields: JSON.stringify(fields)
		}, {
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			setSuccess(`Task '${taskName}' created successfully!`)
			setCode("");
			setTaskName("");
			setDescription("");
			setFields([]);
			setLoading(false);
		})
		.catch(error => {
			console.error(error);
			if (error.response.status === 400) {
				setError(error.response.data.detail);
			} else if (error.response.status === 401) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setCode("");
			setLoading(false)
		});
	}
	
	return (
		<div className="Navigation">
			<Navbar collapseOnSelect expand="sm" variant="dark">
				<Container>
					<Navbar.Brand href="/"><b>TomoFlows</b></Navbar.Brand>
					<Navbar.Toggle aria-controls="collapse-nav" />
        			<Navbar.Collapse id="collapse-nav">
						<Nav className="me-auto">
							<Nav.Link href="`${BASE_PREFIX}/`" active={location.pathname == "/"}>Projects</Nav.Link>
							<Nav.Link href="`${BASE_PREFIX}/tasks`" active={location.pathname == "/tasks"}>Tasks</Nav.Link>
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
							<Dropdown.Item onClick={() => setShow(true)}>Create Task</Dropdown.Item>
							<Dropdown.Item href="`${BASE_PREFIX}/profile`">Profile</Dropdown.Item>
							<Dropdown.Item href="`${BASE_PREFIX}/logout`">Logout</Dropdown.Item>
						</DropdownButton>
					</Navbar.Collapse>
				</Container>
			</Navbar>
			<Outlet key={key}/>
			{/* Create Task Modal */}
			<Modal centered show={show} onHide={handleClose}>
				<Modal.Header>
					<Modal.Title>Create Task</Modal.Title>
				</Modal.Header>
				<Modal.Body className="create-task">
					<Form.Control
						disabled={loading}
						value={code}
						onChange={e => setCode(e.target.value)}
						placeholder="Verification Code" 
					/>
					<Form.Control
						disabled={loading}
						value={taskName}
						onChange={e => setTaskName(e.target.value)}
						placeholder="Task Name" 
						maxLength={25}
					/>
					<Form.Control
						disabled={loading}
						value={description}
						onChange={e => setDescription(e.target.value)}
						placeholder="Task Description" 
						maxLength={100}
					/>
					<div className="parameter-heading">
						<Form.Label>Parameters</Form.Label>
						<Button 
							className="primary-button"
							variant="primary"
							size="sm"
							onClick={() => {
								let newFields = [...fields];
								newFields.push({
									name: "",
									type: "",
									default: "",
								})
								setFields(newFields)
							}}
						>
							<PlusLg />
							Add
						</Button>
					</div>
					{fields.length == 0 ?
					<p>
						<small>
							No Parameters added yet.
						</small>
					</p>
					:fields.map((field, idx) => 
						<div key={idx} className="parameter-fields">
							<Form.Control
								disabled={loading}
								value={field["name"]}
								onChange={e => {
									let newFields = [...fields];
									newFields[idx]["name"] = e.target.value
									setFields(newFields)
								}}
								placeholder="Name" 
								maxLength={25}
								size="sm"
							/>
							<Form.Select
								className={field["type"].length == 0 ? "unset type": "type"}
								disabled={loading}
								value={field["type"]}
								onChange={e => {
									let newFields = [...fields];
									newFields[idx]["type"] = e.target.value
									if (e.target.value === "file")
										newFields[idx]["default"] = null;
									else
										newFields[idx]["default"] = "";
									setFields(newFields)
								}}
								size="sm"
							>
								<option value="">Type</option>
								<option value="string">String</option>
								<option value="number">Number</option>
								<option value="file">File</option>
							</Form.Select>
							{field["type"] === "file" ?
							<Form.Control
								disabled
								value="N/A"
								placeholder="Default Value"
								size="sm"
							/>
							:<Form.Control
								disabled={loading}
								type={field["type"]}
								value={field["default"]}
								onChange={e => {
									let newFields = [...fields];
									newFields[idx]["default"] = e.target.value
									setFields(newFields)
								}}
								placeholder="Default Value" 
								maxLength={25}
								size="sm"
							/>
							}
							<Button
								className="parameter-delete"
								variant="outline-danger"
								size="sm"
								onClick={() => {
									let newFields = [...fields];
									newFields.splice(idx, 1)
									setFields(newFields)
								}}
							>
								<Trash />
							</Button>
						</div>)
					}
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
						className="create-task-button"
						variant="primary"
						onClick={createTask}
						disabled={
							code.length == 0 ||
							taskName.length == 0 ||
							description.length == 0
						}
					>
						{
							loading ?
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
	)
}

export default Navigation;
