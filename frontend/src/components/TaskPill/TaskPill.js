import React from "react";
import { CheckCircle, Hourglass, XCircle } from "react-bootstrap-icons"
import {useDraggable} from '@dnd-kit/core';
import Spinner from 'react-bootstrap/Spinner';
import "./TaskPill.css";

const TaskPill = (props) => {
	const {attributes, listeners, setNodeRef} = props.overlay ? {undefined, undefined, undefined} :
	useDraggable({
		id: `task_pill_${props.task.id}`,
		data: {task: props.task, idx: props.idx}
	});
	return (
		<div
			className={"TaskPill " + (props.idx === props.selected ? "selected" : "")}
			ref={setNodeRef}
			onClick={() => props.onClick()}
			{...listeners}
			{...attributes}
		>	
			<div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "start"}}>
				<h6 style={{width: 230, marginBottom: 0, whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden"}}>{props.task.task.name}</h6>
				<small className="text-body-secondary id"><b>ID: {props.task.run.id}</b></small>
			</div>
			
			{props.task.run.status === "FAILED" ?
				<XCircle size={30} color="red"/> :
			props.task.run.status === "SUCCESS" ?
				<CheckCircle size={30} color="green"/> :
			props.task.run.status === "CREATED" ?
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

export default TaskPill
