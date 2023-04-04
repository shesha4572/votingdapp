import React from "react";
import logo from "../images/voting-logo.png";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField'

const btn = {
    fontSize: '1.2vw',
    backgroundColor: '#45A29E',
    padding: '10px',
    width: '10vw',
    '&:hover': {
        backgroundColor: '#327e79'
    }
}


const input = {
    '.MuiInputBase-input': { fontSize: '1.5rem' },
    width: '15vw',
    height: '3vh',
    '.MuiInputLabel-root': {
        fontSize:'1.5rem'
    }
}
export default function Login() {
    return(
        <>
        <div id="login-mid-box" >
            <div id="login-left">
                <img src={logo} alt="test"/>
                <p>Votechain <br/> The Future of Voting</p>
            </div>

            <div id="login-right">
                <p>Login</p>
                <TextField  sx={input} label="Email" variant="standard" type="email" required/>
                <TextField  sx={input} label="Password" variant="standard" type="password" required/>

                <div id="login-small-buttons">
                    <Button variant='text'>Register</Button>
                    <Button variant='text'>Admin Login</Button>
                </div>

                <Button variant="contained" size="14px" id="login-button" type="submit" sx={btn}>
                    Login
                </Button>
            </div>
        </div>
        </>
    )
}
