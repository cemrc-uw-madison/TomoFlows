import React from 'react'
import Container from 'react-bootstrap/esm/Container'
import { Card, CardActions, CardContent, CardHeader, Typography, Box } from '@mui/material'
import { Button } from '@mui/material'
import "./ResetPassword.css";
import Form from 'react-bootstrap/Form';
import { useState } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
const ResetPassword = () => {
    
    const [newPassword1, setNewPassword1] = useState("");
    const [newPassword2, setNewPassword2] = useState("");
    const navigate = useNavigate();
    const resetPassword = () => {
        let token = Cookies.get("auth-token");
        axios.post("/api/auth/password/change/", {
            new_password1: newPassword1,
            new_password2: newPassword2
        }, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }).then((response) => {
            setNewPassword1("");
            setNewPassword2("");
            toast.success(response.data["detail"]);
         
        }).catch(error => {
            toast.error(error.response.data["new_password2"][0]);
        })
    }
    return (
        <div className='reset-password'>
            <div className='card-layout'>
                <Card className="reset-card">
                    <CardContent className='lead'>
                        <p>
                            Reset your password
                        </p>
                        
                    </CardContent>
                    <CardContent>
                    <div className='reset-password-form'>
                            
                            <Form.Control
                                value={newPassword1}
                                onChange={e=>setNewPassword1(e.currentTarget.value)}
                                placeholder="Enter new password" 
                            />
                            <Form.Control
                                value={newPassword2}
                                onChange={e=>setNewPassword2(e.currentTarget.value)}
                                placeholder="Confirm new password" 
                            />
                        </div>
                    </CardContent>
                    <CardActions className='reset-form-actions'>
                            <Button variant='contained' onClick={resetPassword}>
                                reset
                            </Button>
                    </CardActions>
                </Card>
            </div>
        </div>
    )
}

export default ResetPassword
