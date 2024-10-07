import axios from 'axios';
import Cookies from 'js-cookie';
import React from 'react'
import { useState, useEffect } from 'react'
import Container from 'react-bootstrap/esm/Container';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import "./CreateAccount.css";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import { AccordionActions, Typography } from '@mui/material';
import { Button } from '@mui/material';
import { List, ListItem, ListItemText} from '@mui/material';
import { Divider } from '@mui/material';
import Modal from 'react-bootstrap/Modal';
import { Box } from '@mui/material';
const CreateAccount = () => {
  const [pendingAccounts, setPendingAccounts] = useState([]);
  const [open, setOpen] = useState(false);
  const [password, setPassword] = useState("");
  let token = Cookies.get("auth-token");
  const navigate = useNavigate();
  useEffect(()=>{
   if (token) {
    axios.get("/api/create-account", {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(response=>{
        setPendingAccounts(response.data);
    })
   }
   if (localStorage.getItem("approveStatus")) {
    toast.success("account got approved");
    localStorage.removeItem("approveStatus");
   } 
   if (localStorage.getItem("rejectStatus")) {
    toast.success("account got rejected");
    localStorage.removeItem("rejectStatus");
   }
  }, [])
  const approve = (e) => {
    if (window.confirm("Do you want to approve this account?")) {
        let email = e.currentTarget.value;
        axios.post("/api/create-account", {
            email: email
        }, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }).then(response=>{
            localStorage.setItem("approveStatus", "1");
            setPassword(response.data["password"]);
            setOpen(true);
        })
    }
  }

  const handleClose = () => {
    window.location.reload();
  }

  const reject= (e) => {
    if (window.confirm("Do you want to reject this account?")) {
        let email = e.currentTarget.value;
        axios.delete("/api/create-account", {
            params: {email: email}
        }, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }).then(response=>{
            localStorage.setItem("rejectStatus", "1");
            window.location.reload();
        })
    }
  }

  return (
    <div className='requests'>
        <Container>
            
            <h2 id="request-header">Manage account requests</h2>
            <div className='accordion' id="request-accordion">
               <Modal centered show={open} onHide={handleClose}>
                <Modal.Body>
                    <Typography>Password for this account is {password}</Typography>
                </Modal.Body>
               </Modal>
                {pendingAccounts.length > 0
                ? pendingAccounts.map((pendingAccount)=>{
                    return (
                        <Accordion key={pendingAccount.email}>
                            <AccordionSummary>
                                <p>
                                    <strong>{pendingAccount.first_name} {pendingAccount.last_name} </strong> requested at {pendingAccount.date_joined}
                                </p>
                            </AccordionSummary>
                            <AccordionDetails>
                                <List>
                                    <Divider sx={{opacity: 1}}/>
                                    <ListItem>First Name: {pendingAccount.first_name}</ListItem>
                                    <ListItem>Last Name: {pendingAccount.last_name}</ListItem>
                                    <ListItem>Email Address: {pendingAccount.email}</ListItem>
                                    <ListItem>Lab Name: {pendingAccount.labName}</ListItem>
                                    <ListItem>Institution Name: {pendingAccount.institutionName}</ListItem>
                                    <Divider sx={{opacity: 1}}/>
                                </List>
                                <AccordionActions>
                                    <Button variant="contained" color="error" onClick={reject} value={pendingAccount.email}>Reject</Button>
                                    <Button variant="contained" color="success" onClick={approve} value={pendingAccount.email}>Approve</Button>
                                </AccordionActions>
                            </AccordionDetails>
                        </Accordion>
                    )
                })
                :<Typography>
                        No pending requests
                </Typography>}
            </div>
        </Container>
    </div>
  )
}

export default CreateAccount
