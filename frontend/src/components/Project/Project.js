import React from "react";
import { PlusCircle } from "react-bootstrap-icons";
import "./Project.css";

const Project = (props) => {
	return (
		<div className="Project">
			{props.createProject ? 
			<div className="create">
				<PlusCircle size={45} />
				<small className="description">
					Create Project
				</small>
			</div> :
			<>
				<h4>{props.title}</h4>
				<p><small className="text-body-secondary description">
					{props.description}
				</small></p>
				<small className="last-update">
					Last updated {props.lastUpdate} ago
				</small>
			</>}
		</div>
	)
}

export default Project;
