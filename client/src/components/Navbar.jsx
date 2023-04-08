import React from "react";
import Logo from "../images/voting-logo.png";
import Button from "@mui/material/Button";

const btn = {
    fontSize : '1.5rem',
    color : '#C5C6C7'
}
export const Navigator = () => {
    return(
        <nav>
            <div id="nav-left">
            <img src={Logo} alt="logo" id="nav-logo"/>
            <Button className="nav-btn" sx={btn}>Profile</Button>
            <Button className="nav-btn" sx={btn}>Voting</Button>
            <Button className="nav-btn" sx={btn}>Result</Button>
            </div>
            <Button className="nav-btn" id='logout-btn' sx={btn}>Logout</Button>
        </nav>
    )
}