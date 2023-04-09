import React,{useState} from "react";
import {Navigator} from "./Navbar";
import {Container} from "@mui/material";
import {Card} from "./Card";
import {useEffect} from "react";
import axios from "axios";
import Symbol from "../images/candidate-sym-1.jpg";
import Button from "@mui/material/Button";


const btn = {
    fontSize : '1.5rem',
    color : '#f0f7ff',
    backgroundColor:'#2B9D82FF',
    '&:hover' : {
        backgroundColor: '#217964'
    }
}

export const Voting = () => {

    const[Candidates, setCandidates] = useState([])
   useEffect(() => {
       axios.get("http://localhost:8000/allCandidates").then(res => {if (res.status === 200){setCandidates(res.data.candidates); console.log(Candidates)}})
   },[])


    return (
        <div>
            <Navigator />
            <Container id='voting-cont'>
                {
                    Candidates.map(element =>{
                        return(
                        <div className='card2'>
                            <img src={element.party_photo_url} alt="candidate symbol" className='card2-img'/>
                            <div className='card2-content'>
                            <p>{element.name}</p>
                            <Button className="card2-vote-btn" variant="contained" sx={btn} id={element.id}>Vote</Button>
                            </div>
                        </div>
                        )
                    })
                }

            </Container>
        </div>
    )
}