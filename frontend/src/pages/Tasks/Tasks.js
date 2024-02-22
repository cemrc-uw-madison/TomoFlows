import React, { useState, useEffect }from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import TaskCard from "../../components/TaskCard/TaskCard";
import "./Tasks.css"

/**
 * Tasks component that shows the user their dashboard with relevant features
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Tasks = (props) => {
	// Initialize state variables and hooks
	const [tasks, setTasks] = useState([])
	const [projects, setProjects] = useState([])
	const [loading, setLoading] = useState(true);
	const [addLoading, setAddLoading] = useState(false);
	const [success, setSuccess] = useState("");
	const [projectId, setProjectId] = useState(null);
	const [projectTaskId, setProjectTaskId] = useState(null);
	const [error, setError] = useState("");
	const navigate = useNavigate();
	
	useEffect(() => fetchAllTasks(), [])
	
	const fetchAllTasks = () => {
		let token = Cookies.get('auth-token')
		if (token) {
			setLoading(true);
			axios.get(`/api/tasks`, {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => {
				setTasks(response.data);
				axios.get(`/api/projects`, {
					headers: {
						'Authorization': `Bearer ${token}`
					}
				})
				.then(response => {
					setProjects(response.data);
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
	
	const addTaskToProject = (taskId, projectId) => {
		let token = Cookies.get('auth-token')
		setAddLoading(true);
		axios.post(`/api/project-tasks`,
		{
			project_id: projectId,
			task_id: taskId
		},
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			setProjectId(projectId);
			setProjectTaskId(response.data.id)
			setAddLoading(false);
			setSuccess("Task added to project successfully!")
		})
		.catch(error => {
			console.error(error);
			if (error.response.status in [401, 403, 404]) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setAddLoading(false);
		});
	}
	
	return (
		<div className="Tasks">
			<Container>
				<h2 className="heading"><b>Tasks</b></h2>
				{error.length != 0 && 
					<Alert variant="danger" onClose={() => setError("")} dismissible>
						{error}
					</Alert>
				}
				{success.length != 0 &&
					<Alert variant="success" onClose={() => {
						setSuccess("");
						setProjectId(null);
						setProjectTaskId(null);
					}} dismissible>
						{success}{" "}
						{projectId && 
							<a 
								style={{color: "inherit"}}
								href={`/project/${projectId}?selected=${projectTaskId}`}
							>
								View Task
							</a>
						}
					</Alert>
				}
				{addLoading &&
					<Alert variant="primary">
						Adding Task to Project...
					</Alert>
				}
				<div className="cards">
				{loading ? 
					<Spinner animation="border" variant="primary" /> :
					<>
						{tasks.length === 0 && <p>No Tasks available at the moment.</p>}
						{
							tasks.map((task, idx) => 
								<TaskCard
									key={task.id}
									task={task}
									projects={projects}
									addToProject={addTaskToProject}
								/>
							)
						}
					</>
				}
				</div>
			</Container>
		</div>
	);
};

export default Tasks;
