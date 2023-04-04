import React from 'react'
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button"

const btn = {
    fontSize : '2rem',
    backgroundColor:'#2b9d82',
    '&:hover': {
        backgroundColor:'#2d8d79'
    }
}

const input = {
    '.MuiInputBase-input': { fontSize: '1.5rem' },
    '.MuiInputLabel-root': {
        fontSize:'1.5rem'
    }
}

export default function Register () {
    return (
        <div id='reg-background'>

    <div id="reg-center-box">

        <div id="reg-Top-text">
            <p>Sign up</p>
        </div>

        <div id="reg-Form-top">

            <div id="reg-Form-top-left">
                <TextField className="Text-input" sx={input} variant='standard' type="text"  id="First-name" label="First Name" required/>
                <TextField className="Text-input" sx={input} variant='standard' type="date"  id="DOB" label="Date of Birth" value='1' required/>
            </div>

            <div id="reg-Form-top-right">
                <TextField className="Text-input" sx={input} variant='standard' type="text" id="Last-name" label="Last Name" required/>
                <TextField className="Text-input" sx={input} variant='standard' type="number" id="Phone-no" label="Contact Number" required/>
            </div>
        </div>

        <div id="reg-Form-bottom">
            <TextField className="Text-input2" sx={input} variant='standard' type="text" id="Email" label="Email Address" required/>
            <TextField className="Text-input2" sx={input} variant='standard' type="text" id="number" label="Aadhar number" required/>
            <TextField className="Text-input2" sx={input} variant='standard' type="password" id="Password" label="Create a password" required/>
        </div>
        <Button id="Register-button" variant='contained' sx={btn}>Register</Button>
    </div>
        </div>
    )
}
