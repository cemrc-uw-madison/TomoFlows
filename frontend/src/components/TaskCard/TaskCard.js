import React, { useState } from "react";
import { useNavigate } from "react-router-dom"
import { BoxArrowUpRight, PlusCircle } from "react-bootstrap-icons"
import Button from "react-bootstrap/Button";
import Dropdown from "react-bootstrap/Dropdown";
import Form from "react-bootstrap/Form";
import "./TaskCard.css";

const CustomMenu = React.forwardRef((
	{children, style, className, "aria-labelledby": labeledBy}, ref) => {
		const [value, setValue] = useState("");
		
		return (
			<div
				ref={ref}
				style={{width: 270, marginTop: 5, padding: 10, ...style}}
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

const TaskCard = (props) => {
	const navigate = useNavigate();
	
	return (
		<div className="TaskCard">
			<h4>{props.task.name}</h4>
			<p>
				<small className="text-body-secondary description">
					{props.task.description}
				</small>
			</p>
			<div className="actions">
				<Button
					className="know-more"
					variant="outline-primary"
					size="sm"
					onClick={() => {}}
				>	
					<BoxArrowUpRight />
					Know More
				</Button>
				<Dropdown>
					<Dropdown.Toggle
						className="add-to-project"
						variant="primary"
						size="sm"
					>	
						<PlusCircle />
						Add To Project
					</Dropdown.Toggle>
					<Dropdown.Menu as={CustomMenu} align="end">
						{props.projects.map((project, idx) => 
							<Dropdown.Item key={project.id} onClick={() => props.addToProject(props.task.id, project.id)}>
								{project.name}
							</Dropdown.Item>
						)}
					</Dropdown.Menu>
				</Dropdown>
			</div>
		</div>
	)
}

export default TaskCard;
