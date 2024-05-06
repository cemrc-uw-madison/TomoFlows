import React from "react";
import {useDroppable} from '@dnd-kit/core';
import "./TaskDrop.css";

const TaskDrop = (props) => {
	const {isOver, setNodeRef} = useDroppable({
		id: `task_drop_${props.idx}`,
	});
	
	return (
		<div
			className="TaskDrop"
			ref={setNodeRef}
			style={{backgroundColor: isOver ? "#38023b14": undefined}}
		>
			drag & drop task here
		</div>
	)
}

export default TaskDrop
