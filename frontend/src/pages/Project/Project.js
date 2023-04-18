import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, BoxArrowUpRight, CheckCircle, Hourglass, PencilSquare, PlayFill, PlusCircle, Trash, XCircle } from "react-bootstrap-icons"
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from "react-bootstrap/Container";
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from "react-bootstrap/Button";
import Spinner from 'react-bootstrap/Spinner';
import Dropdown from 'react-bootstrap/Dropdown';
import Badge from 'react-bootstrap/Badge';
import Alert from 'react-bootstrap/Alert';
import "./Project.css";

const CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
	<div
		ref={ref}
		onClick={(e) => {
			e.preventDefault();
			onClick(e);
		}}
		className="task-card add-task"
	>
		<small>Add Task to Project</small>
		<PlusCircle size={30} />
	</div>
));

const CustomMenu = React.forwardRef((
	{children, style, className, "aria-labelledby": labeledBy}, ref) => {
	const [value, setValue] = useState("");
	
	return (
		<div
			ref={ref}
			style={{width: 300, marginTop: 5, padding: 10, ...style}}
			className={className}
			aria-labelledby={labeledBy}
		>
			<Form.Control
				autoFocus
				className="mb-2 w-100"
				placeholder="Search..."
				onChange={(e) => setValue(e.target.value)}
				value={value}
			/>
			<ul className="list-unstyled" style={{marginBottom: 0}}>
				{React.Children.toArray(children).filter(
				(child) =>
					!value || child.props.children.toLowerCase().includes(value.toLowerCase())
				)}
			</ul>
		</div>
	);
	}
  );

const Project = (props) => {
	const { id } = useParams();
	const [project, setProject] = useState({});
	const [allTasks, setAllTasks] = useState([]);
	const [tasks, setTasks] = useState([]);
	const [selected, setSelected] = useState(0);
	const [loading, setLoading] = useState(true);
	const [editLoad, setEditLoad] = useState(false);
	const [deleteLoad, setDeleteLoad] = useState(false);
	const [show, setShow] = useState(false);
	const [showDelete, setShowDelete] = useState(false);
	const [showDeleteTask, setShowDeleteTask] = useState(false);
	const [taskId, setTaskId] = useState(-1);
	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");
	const navigate = useNavigate();
	
	useEffect(() => {
		fetchProject();
	}, [])
	
	const fetchProject = (projecttaskId = null) => {
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
				axios.get(`/api/project-tasks?project_id=${id}`, {
					headers: {
						'Authorization': `Bearer ${token}`
					}
				})
				.then(response => {
					console.log(response.data)
					setTasks(response.data)
					if (projecttaskId !== null) {
						for (let i = 0; i < response.data.length; i++) {
							if (response.data[i].id === projecttaskId) {
								setSelected(i)
							}
						}
					}
					axios.get(`/api/tasks`, {
						headers: {
							'Authorization': `Bearer ${token}`
						}
					})
					.then(response => {
						setAllTasks(response.data);
						setLoading(false);
						setTimeout(() => {
							let selectedDiv = document.querySelector(".task-card.selected")
							if (selectedDiv)
								selectedDiv.scrollIntoView({behavior: "smooth"})
						}, 1000)
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
				})
				.catch(error => {
					setLoading(false);
					if (error.repsonse.status === 404) {
						navigate("/");
					}
					else if (error.response.status === 401 || error.response.status === 403) {
						Cookies.remove('auth-token');
						Cookies.remove('auth-user');
						navigate("/login");
					}
					console.error(error);
				})
			})
			.catch(error => {
				setLoading(false);
				if (error.response.status === 401 || error.response.status === 403) {
					Cookies.remove('auth-token');
					Cookies.remove('auth-user');
					navigate("/login");
				} else if (error.response.status === 404) {
					navigate("/")
				}
				console.error(error);
			})
		} else {
			Cookies.remove('auth-token');
			Cookies.remove('auth-user');
			navigate("/login");
		}
	}
	
	const fetchTasksBackground = () => {
		let token = Cookies.get('auth-token')
		axios.get(`/api/project-tasks?project_id=${id}`, {
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			setTasks(response.data)
			for (let i = 0; i < response.data.length; i++) {
				if (response.data[i].run.status === "RUNNING") {
					setTimeout(() => fetchTasksBackground(), 4000);
					break;
				}
			}
		})
		.catch(error => {
			if (error.repsonse.status === 404) {
				navigate("/");
			}
			else if (error.response.status === 401 || error.response.status === 403) {
				Cookies.remove('auth-token');
				Cookies.remove('auth-user');
				navigate("/login");
			}
			console.error(error);
		})
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
	
	const addTaskToProject = (taskId) => {
		let token = Cookies.get('auth-token')
		setError("");
		axios.post(`/api/project-tasks`,
		{
			project_id: id,
			task_id: taskId
		},
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			let newId = response.data.id
			fetchProject(newId);
		})
		.catch(error => {
			console.log(error);
			if (error.response.status in [401, 403, 404]) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
		});
	}
	
	const runTask = async (projecttaskId) => {
		let token = Cookies.get('auth-token')
		setError("");
		axios.get(`/api/run-project-task/${projecttaskId}`,
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			fetchTasksBackground()
		})
		.catch(error => {
			console.log(error);
			if (error.response.status in [401, 403, 404]) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
		});
	}
	
	const deleteTask = () => {
		let token = Cookies.get('auth-token')
		setDeleteLoad(true);
		setError("");
		axios.delete(`/api/project-tasks/${taskId}`,
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			setDeleteLoad(false);
			setSuccess("Task deleted successfully!")
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
	
	const handleDeleteTaskClose = () => {
		fetchProject();
		setSelected(0);
		setTaskId(-1);
		setError("");
		setSuccess("");
		setShowDeleteTask(false);
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
					<div>
						<div className="heading">
							<div>
								<h5>Tasks</h5>
							</div>
							<div className="button-div">
								{selected !== 0 && 
									<Button
										variant="link"
										size="sm"
										onClick={() => {
											if (selected > 0)
												setSelected(selected => selected - 1)
											let selectedDiv = document.querySelector(".task-card.selected")
											if (selectedDiv)
												selectedDiv.scrollIntoView({
													behavior: "smooth",
													block: "center",
													inline: "end"
												})
										}}
									>	
										<ArrowLeft className="next-button" />
									</Button>
								}
								{selected !== tasks.length - 1 && 
									<Button
										variant="link"
										size="sm"
										onClick={() => {
											if (selected < tasks.length - 1)
												setSelected(selected => selected + 1)
											let selectedDiv = document.querySelector(".task-card.selected")
											if (selectedDiv)
												selectedDiv.scrollIntoView({
													behavior: "smooth",
													block: "center",
													inline: "start"
												})
										}}
									>	
										<ArrowRight className="next-button" />
									</Button>
								}
							</div>
						</div>
						<Dropdown>
							<div className="task-cards">
								{
									tasks.map((task, idx) => 
										<div 
											onClick={() => setSelected(idx)}
											className={"task-card " + (idx === selected ? "selected" : "")}
											key={task.id}
										>
											<h5>{task.task.name}</h5>
											{task.run.status === "FAILED" ?
												<XCircle size={30} color="red"/> :
											task.run.status === "SUCCESS" ?
												<CheckCircle size={30} color="green"/> :
											task.run.status === "CREATED" ?
												<Hourglass size={25} color="black"/> :
												<Spinner
													className="running"
													as="span"
													animation="border"
													size="sm"
													role="status"
													aria-hidden="true"
												/>
											}
										</div>
									)
								}
								<Dropdown.Toggle as={CustomToggle} />
							</div>
							<Dropdown.Menu as={CustomMenu} align="end">
								{allTasks.map((task, idx) => 
									<Dropdown.Item key={task.id} onClick={() => addTaskToProject(task.id)}>
										{task.name}
									</Dropdown.Item>
								)}
							</Dropdown.Menu>
						</Dropdown>
						{tasks[selected] && <div className="task-details">
							<div className="heading">
								<div>
									<h5>Description</h5>
									<small className="text-body-secondary">{tasks[selected].task.description}</small>
								</div>
								<div className="button-div">
									<Button
										className="know-more"
										variant="outline-primary"
										size="sm"
										onClick={() => {}}
									>	
										<BoxArrowUpRight />
										Know More
									</Button>
									{tasks[selected].run.status === "SUCCESS" && 
										<Button
											variant="outline-success"
											size="sm"
										>	
											<CheckCircle />
											Run: Success
										</Button>
									}
									{tasks[selected].run.status === "FAILED" && 
										<Button
											variant="outline-danger"
											size="sm"
										>	
											<XCircle />
											Run: Failed
										</Button>
									}
									{tasks[selected].run.status === "CREATED" && 
										<Button
											variant="outline-dark"
											size="sm"
										>	
											<Hourglass />
											Pending Run
										</Button>
									}
									<Button
										className={tasks[selected].run.status !== "RUNNING" && "primary-button"}
										variant={tasks[selected].run.status === "RUNNING" ? "secondary" : "primary"}
										size="sm"
										disabled={tasks[selected].run.status === "RUNNING"}
										onClick={() => runTask(tasks[selected].id)}
									>	
										{tasks[selected].run.status === "RUNNING" ? 
											<Spinner
												className="button-spinner"
												as="span"
												animation="border"
												size="sm"
											/> : 
											<PlayFill size={20} style={{marginLeft: -2, marginRight: 2}}/>}
										{tasks[selected].run.status === "RUNNING" ? "Running" : "Run Task"}
									</Button>
									<Button
										variant="outline-danger"
										size="sm"
										onClick={() => {
											setTaskId(tasks[selected].id)
											setShowDeleteTask(true);
										}}
									>	
										<Trash style={{marginRight: -1, marginTop: -1}}/>
									</Button>
								</div>
							</div>
							<div className="parameters">
								<h5>Parameters</h5>
								<div className="input-fields">
									<Form.Group>
										<Form.Label>Parameter X</Form.Label>
										<Form.Control size="sm" placeholder="enter parameter value" />
									</Form.Group>
									<Form.Group>
										<Form.Label>Parameter Y</Form.Label>
										<Form.Control size="sm" placeholder="enter parameter value" />
									</Form.Group>
									<Form.Group>
										<Form.Label>Parameter Z</Form.Label>
										<Form.Control size="sm" placeholder="enter parameter value" />
									</Form.Group>
								</div>
							</div>
							{
								tasks[selected].run.status === "RUNNING" ? 
								<div className="div" style={{flexDirection: "column", alignItems: "center"}}>
									<Spinner animation="border" variant="primary" style={{width: 70, height: 70, margin: "80px auto", marginBottom: 15}} />
									<small>Running Task</small>
								</div> :
								<div className="last-run">
									<h5>Run</h5>
									{tasks[selected].run.status === "CREATED" ? 
										<small>Task has not been run yet. Click on 'Run Task' to run the task</small> :
										<div className="button-div" style={{gap: 20}}>
											<div className="logs">
												<small>Logs</small><br/>
												{
													tasks[selected].run.logs &&
													tasks[selected].run.logs.map((log, idx) => 
														<small className="text-body-secondary" key={idx}>
															{log.timestamp}: {log.detail}<br/>
														</small>
													)
												}
											</div>
											<div className="errors">
												<small>Errors</small><br/>
												{
													tasks[selected].run.errors.length === 0 ?
													<small className="text-body-secondary">No Errors logged for this run</small> :
													tasks[selected].run.errors.map((error, idx) => 
														<div className="error-badge" key={idx}>
															<b>{error.type}</b>
															<small>{error.detail}</small>
														</div>
													)
												}
											</div>
										</div>
									}
								</div>
							}
						</div>}
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
			<Modal centered show={showDeleteTask} onHide={handleDeleteTaskClose}>
				<Modal.Header>
					<Modal.Title>Delete Task</Modal.Title>
				</Modal.Header>
				<Modal.Body className="edit-project">
					<p>
						Are you sure you want to delete this task? 
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
					<Button variant="secondary" onClick={handleDeleteTaskClose}>
						Cancel
					</Button>
					<Button
						className="delete-project-button"
						variant="danger"
						onClick={deleteTask}
						disabled={success === "Task deleted successfully!"}
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
