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
import { AccordionActions } from '@mui/material';
import {Button} from '@mui/material';
import {List, ListItem, ListItemText} from '@mui/material';

const CreateAccount = () => {
  const [pendingAccounts, setPendingAccounts] = useState([]);
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
            toast.success(response.data["message"] + `\nuser password is ${response.data["password"]}`);

            // window.location.reload();
        })
    }
  }
  
  const reject= (e) => {
    if (window.confirm("Do you want to reject this account?")) {

    }
  }

  return (
    <div className='requests'>
        <Container>
            
            <h2>Manage account requests</h2>
            <div className='accordion' id="request-accordion">
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
                                    <ListItem>First Name: {pendingAccount.first_name}</ListItem>
                                    <ListItem>Last Name: {pendingAccount.last_name}</ListItem>
                                    <ListItem>Email Address: {pendingAccount.email}</ListItem>
                                    <ListItem>Lab Name: {pendingAccount.labName}</ListItem>
                                    <ListItem>Institution Name: {pendingAccount.institutionName}</ListItem>
                                </List>
                                <AccordionActions>
                                    <Button variant="contained" color="error" onClick={reject}>Reject</Button>
                                    <Button variant="contained" color="success" onClick={approve} value={pendingAccount.email} data-toggle="confirmation">Approve</Button>
                                </AccordionActions>
                            </AccordionDetails>
                        </Accordion>
                    )
                })
                :<text>
                        No pending request
                </text>}
            </div>
        </Container>
    </div>
  )
}

export default CreateAccount
