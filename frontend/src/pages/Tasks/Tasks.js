import React from "react";
import { useNavigate } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import "./Tasks.css"

/**
 * Pipelines component that shows the user their dashboard with relevant features
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Tasks = (props) => {
	// Initialize state variables and hooks
	const navigate = useNavigate();					// navigation hook
	
	return (
		<div className="Tasks">
			<Container>
				<h2><b>Tasks</b></h2>
				Under Construction. Come back later!
			</Container>
		</div>
	);
};

export default Tasks;
