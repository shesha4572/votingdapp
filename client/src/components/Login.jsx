import React from "react";
import logo from "../images/voting-logo.png";
import Button from '@mui/material/Button';
// import Input from '@mui/material/Input'
import TextField from '@mui/material/TextField'
export default function Login() {
    return(
        <>
        <div id="mid-box">
            <div id="login-left">
                <img src={logo} alt="test"/>
                <p>Votechain <br/> The Future of Voting</p>
            </div>

            <div id="login-right">
                <p>Login</p>
                <TextField id="outlined-basic" label="Email" variant="outlined" />
                <TextField id="outlined-basic" label="Password" variant="outlined" />

                <Button variant="contained" size="large">Login</Button>
            </div>
        </div>
        </>
    )
}
