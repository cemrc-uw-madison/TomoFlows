import React, { useState, useEffect }from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';
import Button from "react-bootstrap/esm/Button";
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
		let toastId = toast.loading("Adding task to project...")
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
			toast.success((t) => (
				<span>
					{"Task added successfully "}
					{response.data.id && 
						<Button
							variant="light"
							size="sm"
							onClick={() => navigate(`/project/${projectId}?selected=${response.data.id}`)}
						>
							View Task
						</Button>
					}
				</span>
			), {duration: 6000});
		})
		.catch(error => {
			console.error(error);
			if (error.response.status in [401, 403, 404]) {
				toast.error(error.response.data.detail)
			} else {
				toast.error("Something went wrong! Please try again later.")
			}
		})
		.finally(() => {
			toast.dismiss(toastId);
		});
	}
	
	return (
		<div className="Tasks">
			<Container>
				<h2 className="heading"><b>Tasks</b></h2>
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
