import React from "react";
import {Navigator} from "./Navbar";
import {Container} from "@mui/material";
import {Card} from "./Card";

export const Voting = () => {
    return (
        <div>
            <Navigator />
            <Container id='voting-cont'>
                <Card />
                <Card />
                <Card />
                <Card />
            </Container>
        </div>
    )
}