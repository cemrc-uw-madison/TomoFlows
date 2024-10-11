import axios from 'axios';
import Cookies from 'js-cookie';
import React from 'react'
import { useState, useEffect } from 'react'
import Container from 'react-bootstrap/esm/Container';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import "./ManageAccount.css";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import { AccordionActions, Typography } from '@mui/material';
import { Button } from '@mui/material';
import { List, ListItem, ListItemText} from '@mui/material';
import { Divider } from '@mui/material';
import Modal from 'react-bootstrap/Modal';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import { Box } from '@mui/material';

const ManageAccount = () => {
  const [pendingAccounts, setPendingAccounts] = useState([]);
  const [activeAccounts, setActiveAccounts] = useState([]);
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
   axios.get("/api/active-userlist", {
    headers: {
        'Authorization': `Bearer ${token}`
    }
   }).then((response) => {
    setActiveAccounts(response.data);
   })
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
  const CustomExpandIcon = () => {
    return (
      <Box
        sx={{
          ".Mui-expanded & > .collapsIconWrapper": {
            display: "none"
          },
          ".expandIconWrapper": {
            display: "none"
          },
          ".Mui-expanded & > .expandIconWrapper": {
            display: "block"
          }
        }}
      >
        <div className="expandIconWrapper">-</div>
        <div className="collapsIconWrapper">+</div>
      </Box>
    );
  };
  return (
    <div className='requests'>
        <Container>
            
            <h2 id="request-header">Manage account requests</h2>
            <div className='accordion' id="request-accordion">
               <Typography sx={{marginBottom: '20px'}} >Pending Requests</Typography>
               <Divider sx={{opacity: 1, marginBottom: '10px'}}></Divider>
                {pendingAccounts.length > 0
                ? pendingAccounts.map((pendingAccount)=>{
                    return (
                        <Accordion key={pendingAccount.email}>
                            <AccordionSummary  expandIcon={<CustomExpandIcon />}>
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
            <Divider sx={{opcaty: 1}}></Divider>
            <div id='active-account'>
                <Typography sx={{marginBottom: '20px'}}>Active Account</Typography>
                <Divider sx={{opacity: 1, marginBottom: '10px'}}></Divider>
                {activeAccounts.length > 0
                ? activeAccounts.map((activeAccount)=>{
                    return (
                        <Accordion key={activeAccount.email}>
                            <AccordionSummary  expandIcon={<CustomExpandIcon />}>
                                <p>
                                    <strong>{activeAccount.first_name} {activeAccount.last_name} </strong>
                                </p>
                            </AccordionSummary>
                            <AccordionDetails>
                                <List>
                                    <Divider sx={{opacity: 1}}/>
                                    <ListItem>First Name: {activeAccount.first_name}</ListItem>
                                    <ListItem>Last Name: {activeAccount.last_name}</ListItem>
                                    <ListItem>Email Address: {activeAccount.email}</ListItem>
                                    <ListItem>Lab Name: {activeAccount.labName}</ListItem>
                                    <ListItem>Institution Name: {activeAccount.institutionName}</ListItem>
                                    <Divider sx={{opacity: 1}}/>
                                </List>
                            </AccordionDetails>
                        </Accordion>
                    )
                })
                :<Typography>
                        No Active Account
                </Typography>}
            </div>
        </Container>
    </div>
  )
}

export default ManageAccount;
