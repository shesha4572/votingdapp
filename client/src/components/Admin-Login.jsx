import React from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

const btn = {
    fontSize : '2rem',
    backgroundColor:'#c3073f',
    '&:hover': {
        backgroundColor:'#9d0933'
    }
}

const input = {
    '.MuiInputBase-input': { fontSize: '1.5rem' },
    width:'18vw',
    '.MuiInputLabel-root': {
        fontSize:'1.5rem'
    }
}

export default function adminLogin () {
    return(
        <div id='admin-login-background'>
            <div id='admin-login-center-box'>

                <div id="admin-login-title">
                    <p>Admin login</p>
                </div>

                <TextField  sx={input} variant='standard' type="text" id="admin-uname" label="Username" required/>
                <TextField  sx={input} variant='standard' type="password" id="admin-pass" label="Password" required/>

                <Button id="admin-login-button" variant='contained' sx={btn}>Login</Button>

            </div>

        </div>
    )
}