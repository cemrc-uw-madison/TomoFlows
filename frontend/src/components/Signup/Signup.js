import React from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import "./Signup.css"

const Signup = (props) => {	
	return (
		<div className="Signup">
			<h1>TomoFlows</h1>
			<h5>Sign Up</h5>
			<div className="signup-form">
				<Form.Control placeholder="Enter email" />
				<Form.Control type="password" placeholder="Enter password" />
				<Form.Control type="password" placeholder="Confirm password" />
				<Button onClick={() => {}}variant="primary">Sign Up</Button>
			</div>
		</div>
	);
};

export default Signup;
