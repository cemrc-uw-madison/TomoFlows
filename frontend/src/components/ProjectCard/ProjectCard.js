import React from "react";
import { useNavigate } from "react-router-dom"
import { PlusCircle } from "react-bootstrap-icons";
import "./ProjectCard.css";

const ProjectCard = (props) => {
	const navigate = useNavigate();
	
	const timeSince = (timestamp) => {
		const seconds = Math.floor((new Date() - new Date(timestamp)) / 1000);
		let interval = Math.floor(seconds / 31536000);
		if (interval >= 1) {
		  return interval == 1 ? "1 year" : interval + " years";
		}
		interval = Math.floor(seconds / 2592000);
		if (interval >= 1) {
		  return interval == 1 ? "1 month" : interval + " months";
		}
		interval = Math.floor(seconds / 604800);
		if (interval >= 1) {
		  return interval == 1 ? "1 week" : interval + " weeks";
		}
		interval = Math.floor(seconds / 86400);
		if (interval >= 1) {
		  return interval == 1 ? "1 day" : interval + " days";
		}
		interval = Math.floor(seconds / 3600);
		if (interval >= 1) {
		  return interval == 1 ? "1 hour" : interval + " hours";
		}
		interval = Math.floor(seconds / 60);
		if (interval >= 1) {
		  return interval == 1 ? "1 minute" : interval + " minutes";
		}
		interval = Math.floor(seconds)
		return interval == 1 ? "1 second" : interval + " seconds";
	}
	
	return (
		<div className="ProjectCard" onClick={
			() => props.createProject ? props.toggle() : navigate(`/project/${props.id}`)
		}>
			{props.createProject ? 
			<div className="create">
				<PlusCircle size={45} />
				<small className="description">
					Create Project
				</small>
			</div> :
			<>
				<h4>{props.name}</h4>
				<p><small className="text-body-secondary description">
					{props.description}
				</small></p>
				<small className="last-update">
					Last updated {timeSince(props.lastUpdated)} ago
				</small>
			</>}
		</div>
	)
}

export default ProjectCard;
