import React, { useState, useEffect } from "react";
import axios from 'axios';
import Cookies from 'js-cookie';
import Modal from 'react-bootstrap/Modal';
import Button from "react-bootstrap/Button";
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import "./FolderPicker.css";
import { ChevronLeft, ChevronRight, FileEarmarkText, Folder,  } from "react-bootstrap-icons";

const FolderPicker = ({ show, onHide, onSelect }) => {
	const [currentPath, setCurrentPath] = useState('');
	const [currentFullPath, setCurrentFullPath] = useState('');
  	const [contents, setContents] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");
	
	useEffect(() => {
		if (show) {
		  fetchDirectoryContents('');
		}
	}, [show]);
	
	const fetchDirectoryContents = (path) => {
		let token = Cookies.get('auth-token')
		setLoading(true)
		axios.get(`/api/get-directory-contents?path=${path}`, {
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
		.then(response => {
			setContents(response.data["contents"])
			setCurrentFullPath(response.data["full_path"])
			setCurrentPath(response.data["path"])
			setLoading(false)
		})
		.catch(error => {
			console.error(error)
			if (error.response.status === 400 ||error.response.status === 404) {
				setError(error.response.data.detail);
			} else {
				setError("Something went wrong! Please try again later.")
			}
			setLoading(false);
		})
	}
	
	const handleDirectoryClick = (itemName) => {
		const newPath = currentPath ? `${currentPath}/${itemName}` : itemName;
    	fetchDirectoryContents(newPath);
	}
	
	const handleBackClick = () => {
		const newPath = currentPath.substring(0, currentPath.lastIndexOf('/'));
    	fetchDirectoryContents(newPath);
	}
	
	return (
		<Modal scrollable centered show={show} onHide={onHide} className="FolderPicker">
			<Modal.Header>
				<Modal.Title>
					Select Directory
				</Modal.Title>
			</Modal.Header>
			<Modal.Body style={{padding: 5}}>
				{loading ? 
					<div style={{margin: "50px 0px", display: "flex", justifyContent: "center", alignItems: "center"}}>
						<Spinner animation="border" variant="primary" style={{width: 80, height: 80}} />
					</div>
				: contents.length === 0 ?
					<small style={{margin: 10}} className="text-body-secondary">No contents</small>
				: <>
					{currentPath !== "" &&
						<div className="folder-item dir" key={-1} onClick={handleBackClick}>
							<div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
								<ChevronLeft style={{marginLeft: -1, marginRight: 7, marginTop: 1}} size={20} />
								<div>
									Back
								</div>
							</div>
						</div>
					}
					{contents.map((item, idx) => 
						<div 
							className={`folder-item${item.is_directory ? " dir": ""}`}
							key={idx}
							onClick={() => item.is_directory ? handleDirectoryClick(item.item): null}
						>
							<div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
								{item.is_directory ? 
									<Folder style={{marginRight: 7, marginTop: 1}} size={20} /> : 
									<FileEarmarkText style={{marginRight: 7}} size={20} />
								}
								<div style={{ 
									maxWidth: 410, 
									overflow: "hidden",
									whiteSpace: "nowrap",
									textOverflow: "ellipsis"}}
								>
									{item.item}
								</div>
							</div>
							{item.is_directory && 
							<div>
								<ChevronRight size={20} style={{marginBottom: 3}}/>
							</div>}
						</div>
					)}
					{error.length != 0 && 
						<Alert variant="danger" onClose={() => setError("")} dismissible>
							{error}
						</Alert>
					}
				</>
				
			}
			</Modal.Body>
			<Modal.Footer style={{display: "inline-block"}}>
				<div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: "center"}}>
					<div style={{fontSize: 14, marginBottom: 3}}>
						/{currentPath}
					</div>
					<div style={{display: "flex", flexDirection: "row", gap: 10}}>
						<Button variant="secondary" onClick={onHide}>
							Cancel
						</Button>
						<Button
							className="select-button"
							variant="primary"
							onClick={() => onSelect(currentFullPath)}
							disabled={loading}
						>
							{
								loading ?
								<Spinner
									as="span"
									animation="border"
									size="sm"
									role="status"
									aria-hidden="true"
								/> :
								"Select"
							}
						</Button>
					</div>
				</div>
			</Modal.Footer>
		</Modal>
	)
}

export default FolderPicker;
