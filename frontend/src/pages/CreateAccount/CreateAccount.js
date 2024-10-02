import axios from 'axios';
import Cookies from 'js-cookie';
import React from 'react'
import { useState, useEffect } from 'react'
import Container from 'react-bootstrap/esm/Container';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import "./CreateAccount.css";

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
    let email = e.currentTarget.value;
    axios.post("/api/create-account", {
        email: email
    }, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(response=>{
        toast.success(response.data["message"]);
        window.location.reload();
    })
  }
  return (
    <div className='Requests'>
        <Container>
            <h2>Manage account requests</h2>
            <div className='accordion'>
                {pendingAccounts.length > 0
                ? pendingAccounts.map((pendingAccount)=>{
                    return (
                        <div className='accordion-item' key={pendingAccount.email}>
                            {pendingAccount.email}
                            <button onClick={approve} value={pendingAccount.email}>approve</button>
                        </div>
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
