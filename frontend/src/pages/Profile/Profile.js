import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PencilSquare } from "react-bootstrap-icons";
import api from '../api.js';
import Cookies from 'js-cookie';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import "./Profile.css";

const Profile = (props) => {
	const [loading, setLoading] = useState(true);		// API request loading state
	const [editLoad, setEditLoad] = useState(false);		// API edit request loading state
	const [user, setUser] = useState({})				// APR response user state
	const [showEdit, setShowEdit] = useState(false)		// edit user modal open state
	const [firstName, setFirstName] = useState("")		// edit user first name modal input state
	const [lastName, setLastName] = useState("")		// edit user last name modal input state
	const [success, setSuccess] = useState("")			// API response success state
	const [error, setError] = useState("")				// APT reponse error state
	const navigate = useNavigate()						// navigation hook
	
	useEffect(() => fetchUser(), [])
	
	const fetchUser = () => {
		let token = Cookies.get('auth-token')
		if (token) {
			setLoading(true);
			api.get('/user', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			})
			.then(response => {
				setUser(response.data);
				setFirstName(response.data.first_name);
				setLastName(response.data.last_name);
				Cookies.remove('auth-user');
				Cookies.set('auth-user', JSON.stringify(response.data))
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
		} else {
			Cookies.remove('auth-token');
			Cookies.remove('auth-user');
			navigate("/login");
		}
	}
	
	const editUser = () => {
		let token = Cookies.get('auth-token')
		setEditLoad(true);
		setError("")
		api.put(`/user`,
		{
			first_name: firstName,
			last_name: lastName,
		},
		{
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			setEditLoad(false);
			setSuccess(`Profile updated successfully!`)
		})
		.catch(error => {
			setEditLoad(false);
			if (error.response.status === 401 || error.response.status === 403 || error.response.status === 404) {
				setError(error.response.data.detail ?? "Something went wrong! Please try again later.")
			}
			console.error(error);
		})
	}
	
	const handleEditClose = () => {
		fetchUser();
		setShowEdit(false);
		setError("");
		setSuccess("");
		window.location.reload();
	}
	
	return (
		<div className="Profile">
			<Container>
				{loading ?
					<div className="div">
						<Spinner animation="border" variant="primary" /> 
					</div>:
					<>
						<div className="heading">
							<div>
								<h2><b>Profile</b></h2>
							</div>
							<div className="button-div">
								<Button
									className="primary-button"
									variant="primary"
									onClick={() => setShowEdit(true)}
								>	
									<PencilSquare className="manage"/>
									Edit Profile
								</Button>
							</div>
						</div>
						<div>
							<p>
								<b>Name: </b>{user.first_name} {user.last_name}<br/>
								<b>Email: </b>{user.email}<br/>
							</p>
						</div>
					</>
				}
			</Container>
			<Modal centered show={showEdit} onHide={handleEditClose}>
				<Modal.Header>
					<Modal.Title>Edit Profile</Modal.Title>
				</Modal.Header>
				<Modal.Body className="edit-profile">
					<Form.Control
						disabled={editLoad}
						value={firstName}
						onChange={e => setFirstName(e.target.value)}
						placeholder="First Name"
					/>
					<Form.Control
						disabled={editLoad}
						value={lastName}
						onChange={e => setLastName(e.target.value)}
						placeholder="Last Name"
						maxLength={25}
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
					<Button variant="secondary" onClick={handleEditClose}>
						Cancel
					</Button>
					<Button
						className="edit-profile-button"
						variant="primary"
						onClick={editUser}
						disabled={
							firstName.length == 0 ||
							lastName.length == 0
						}
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
							"Edit"
						}
					</Button>
				</Modal.Footer>
			</Modal>
		</div>
	)
}

export default Profile;
