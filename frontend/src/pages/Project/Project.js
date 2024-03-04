import React, { useState, useEffect } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Files, CheckCircle, ChevronBarLeft, ChevronBarRight, Folder, Hourglass, PencilSquare, PlayFill, PlusCircle, Trash, XCircle, FileEarmarkText } from "react-bootstrap-icons"
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from "react-bootstrap/Container";
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from "react-bootstrap/Button";
import Spinner from 'react-bootstrap/Spinner';
import Dropdown from 'react-bootstrap/Dropdown';
import Alert from 'react-bootstrap/Alert';
import InputGroup from 'react-bootstrap/InputGroup';
import toast from 'react-hot-toast';
import "./Project.css";
import FolderPicker from "../../components/FolderPicker/FolderPicker";
import FilePicker from "../../components/FilePicker/FilePicker";

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
			{
					React.Children.toArray(children).length === 0 ?
					<small>No Tasks available at the moment.</small>:
					<>
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
					</>
				}
		</div>
	);
	}
);

const formatDateTime = (date) => {
	const optionsDate = { year: 'numeric', month: '2-digit', day: '2-digit' };
	const dateString = date.toLocaleDateString('en-US', optionsDate);
	const optionsTime = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
	const timeString = date.toLocaleTimeString('en-US', optionsTime);
  	const timeZone = date.toLocaleTimeString('en-US', { timeZoneName: 'short' }).split(' ')[2];
	return `${dateString.replaceAll('/', '-')} ${timeString} ${timeZone}`;
  }

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
	const [showFolderPicker, setShowFolderPicker] = useState(false);
	const [showFilePicker, setShowFilePicker] = useState(false);
	const [taskId, setTaskId] = useState(-1);
	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");
	const [searchParams, setSearchParams] = useSearchParams();
	const navigate = useNavigate();
	
	useEffect(() => {
		fetchProject(parseInt(searchParams.get("selected")));
		setSearchParams({});
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
					let taskList = JSON.parse(JSON.stringify(response.data));
					for (let i = 0; i < taskList.length; i++) {
						if (taskList[i].parameter_values.length === 0) {
							let parameter_fields = JSON.parse(taskList[i].task.parameter_fields)
							taskList[i]["parameter_values"] = parameter_fields.map((field) => field["default"]);
						}
					}
					setTasks(taskList);
					if (projecttaskId !== null) {
						for (let i = 0; i < taskList.length; i++) {
							if (taskList[i].id === projecttaskId) {
								setSelected(i)
							}
						}
					}
					for (let i = 0; i < taskList.length; i++) {
						if (taskList[i].run.status === "RUNNING") {
							setTimeout(() => fetchTasksBackground(), 4000);
							break;
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
								selectedDiv.scrollIntoView({
									behavior: "smooth",
									block: "center",
									inline: "end"
								})
						}, 1000)
					})
					.catch(error => {
						setLoading(false);
						console.error(error);
						if (error.response.status === 401 || error.response.status === 403) {
							Cookies.remove('auth-token');
							Cookies.remove('auth-user');
							navigate("/login");
						}
					})
				})
				.catch(error => {
					setLoading(false);
					console.error(error);
					if (error.response.status === 404) {
						navigate("/");
					}
					else if (error.response.status === 401 || error.response.status === 403) {
						Cookies.remove('auth-token');
						Cookies.remove('auth-user');
						navigate("/login");
					}
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
			let taskList = JSON.parse(JSON.stringify(response.data));
			let taskMap = taskList.reduce((acc, obj) => ({ ...acc, [obj.id]: obj }), {});
			setTasks((oldTasks) => {
				let newTasks = [...oldTasks]
				for (let i = 0; i < newTasks.length; i++) {
					newTasks[i].run = taskMap[newTasks[i].id].run
				}
				return newTasks
			})
			for (let i = 0; i < taskList.length; i++) {
				if (taskList[i].run.status === "RUNNING") {
					setTimeout(() => fetchTasksBackground(), 4000);
					break;
				}
			}
		})
		.catch(error => {
			console.error(error);
			if (error.response.status === 404) {
				navigate("/");
			}
			else if (error.response.status === 401 || error.response.status === 403) {
				Cookies.remove('auth-token');
				Cookies.remove('auth-user');
				navigate("/login");
			}
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
			setSuccess(`Project '${name}' updated successfully!`)
			setEditLoad(false);
		})
		.catch(error => {
			console.error(error);
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
			setShowDelete(false);
			setDeleteLoad(false);
			toast.success("Project deleted successfully")
			navigate("/");
		})
		.catch(error => {
			console.error(error);
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
			toast.success("Task added successfully")
			fetchProject(newId);
		})
		.catch(error => {
			console.error(error);
			if (error.response.status in [401, 403, 404]) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
		});
	}
	
	const runTask = (projecttaskId, parameter_values) => {
		let token = Cookies.get('auth-token')
		setError("")
		axios.put(`/api/project-tasks/${projecttaskId}`,
		{
			parameter_values: JSON.stringify(parameter_values)
		},
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			axios.get(`/api/run-project-task/${projecttaskId}`,
			{
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => {
				fetchTasksBackground()
				toast.success("Task run started")
			})
			.catch(error => {
				console.error(error);
				if (error.response.status in [401, 403, 404]) {
					toast.error(error.response.data.detail);
				} else {
					toast.error("Something went wrong! Please try again later.")
				}
			});
		})
		.catch(error => {
			console.error(error);
			if (error.response.status in [401, 403, 404]) {
				toast.error(error.response.data.detail);
			} else {
				toast.error("Something went wrong! Please try again later.")
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
			toast.success("Task deleted successfully")
			fetchProject();
			setSelected(0);
			setTaskId(-1);
			setError("");
			setSuccess("");
			setShowDeleteTask(false);
			setDeleteLoad(false);
		})
		.catch(error => {
			console.error(error);
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
	
	const handleFolderPickerClose = () => {
		setShowFolderPicker(false);
	}
	
	const handleFolderPickerSelect = (path) => {
		let newTasks = JSON.parse(JSON.stringify(tasks));
		newTasks[selected].parameter_values[showFolderPicker] = path;
		setTasks(newTasks);
		setShowFolderPicker(false);
	}
	
	const handleFilePickerClose = () => {
		setShowFilePicker(false);
	}
	
	const handleFilePickerSelect = (path) => {
		let newTasks = JSON.parse(JSON.stringify(tasks));
		newTasks[selected].parameter_values[showFilePicker] = path;
		setTasks(newTasks);
		setShowFilePicker(false);
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
								<Button
									disabled={tasks.length === 0 || selected === 0}
									variant="link"
									size="sm"
									onClick={() => {
										if (selected > 0)
											setSelected(0)
										let taskCardsDiv = document.querySelector(".task-cards");
										taskCardsDiv.scrollTo({left: 0, behavior: 'smooth'});
									}}
								>	
									<ChevronBarLeft className="next-button" />
								</Button>
								<Button
									disabled={tasks.length === 0 || selected === 0}
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
								<Button
									disabled={tasks.length === 0 || selected === tasks.length - 1}
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
								<Button
									disabled={tasks.length === 0 || selected === tasks.length - 1}
									variant="link"
									size="sm"
									onClick={() => {
										if (selected < tasks.length - 1)
											setSelected(tasks.length - 1)
										let taskCardsDiv = document.querySelector(".task-cards");
										taskCardsDiv.scrollTo({left: taskCardsDiv.scrollWidth, behavior: 'smooth'});
									}}
								>	
									<ChevronBarRight className="next-button" />
								</Button>
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
											<div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "start"}}>
												<h6 style={{width: 230, marginBottom: 0, whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden"}}>{task.task.name}</h6>
												<small className="text-body-secondary id"><b>ID: {task.run.id}</b></small>
											</div>
											
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
									<small className="text-body-secondary">{tasks[selected].task.name}: {tasks[selected].task.description}</small>
								</div>
								<div className="button-div">
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
										onClick={() => runTask(tasks[selected].id, tasks[selected].parameter_values)}
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
									{
										JSON.parse(tasks[selected].task.parameter_fields).length === 0 ?
										<small>No Parameters</small>
										:JSON.parse(tasks[selected].task.parameter_fields).map((item, idx) => 
											<Form.Group key={idx}>
												<Form.Label>{item.name}</Form.Label>
												{item.type === "file" ?
													<InputGroup>
														<Form.Control
															value={tasks[selected].parameter_values[idx] ?? ""}
															size="sm"
															placeholder="select file"
															readOnly
														/>
														<Button
															variant="outline-secondary"
															size="sm"
															onClick={() => {setShowFilePicker(idx)}}
														>
															<Folder />
														</Button>
													</InputGroup>
												: item.type === "directory" ?
												<InputGroup>
													<Form.Control
														value={tasks[selected].parameter_values[idx] ?? ""}
														size="sm"
														placeholder="select directory"
														readOnly
													/>
													<Button
														variant="outline-secondary"
														size="sm"
														onClick={() => {setShowFolderPicker(idx)}}
													>
														<Folder />
													</Button>
												</InputGroup>
												: <Form.Control
													type={item.type}
													value={tasks[selected].parameter_values[idx] ?? ""}
													onChange={(e) => {
														let newTasks = JSON.parse(JSON.stringify(tasks));
														newTasks[selected].parameter_values[idx] = e.target.value;
														setTasks(newTasks)
													}}
													size="sm"
													placeholder="enter parameter value"
												/>}
											</Form.Group>
										)
									}
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
											<div className="logs" style={{maxWidth: "70%"}}>
												<small>Logs</small><br/>
												<div className="log-text" style={{marginTop: 5, maxHeight: 400, overflowY: "scroll", position: "relative"}}>
													{
														tasks[selected].run.logs &&
														tasks[selected].run.logs.map((log, idx) => 
															<small className="text-body-secondary" key={idx}>
																{formatDateTime(new Date(log.timestamp))}: {log.detail}<br/>
															</small>
														)
													}
												</div>
											</div>
											{tasks[selected].run.status === "FAILED" ? 
											<div className="errors">
												<small>Errors</small><br/>
												<div style={{marginTop: 5, maxHeight: 400, overflowY: "scroll"}}>
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
											: <div className="output-files">
												<small>Output Files</small><br/>
												<div style={{marginTop: 5, maxHeight: 400, overflowY: "scroll"}}>
													{
														tasks[selected].run.output_files.length === 0 ?
														<small className="text-body-secondary">No Output files for this run</small> :
														tasks[selected].run.output_files.map((output_file, idx) => 
															<div className="output-file-badge" key={idx} onClick={() => {
																if (output_file.file_name.includes("/home/tomoflows/data")) {
																	navigator.clipboard.writeText(output_file.file_name.replace("/home/tomoflows/data", "/tmp/tomoflows"))
																} else {
																	navigator.clipboard.writeText(output_file.file_name)
																}
															}}>
																<FileEarmarkText style={{marginRight: 5, marginTop: -1}} size={20} />
																<div style={{marginRight: 1}}>{output_file.file_name.split("/").pop()}</div>
															</div>
														)
													}
												</div>
											</div>}
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
						Close
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
						{success.length == 0 ? "Cancel": "Close"}
					</Button>
					{success.length == 0 && <Button
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
					</Button>}
				</Modal.Footer>
			</Modal>
			<FolderPicker
				show={showFolderPicker !== false}
				onHide={handleFolderPickerClose}
				onSelect={handleFolderPickerSelect}
			/>
			<FilePicker
				show={showFilePicker !== false}
				onHide={handleFilePickerClose}
				onSelect={handleFilePickerSelect}
			/>
		</div>
	)
}

export default Project
