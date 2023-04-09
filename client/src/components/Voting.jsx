import React,{useState} from "react";
import {Navigator} from "./Navbar";
import {Container} from "@mui/material";
import {useEffect} from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import Cookies from "universal-cookie";
import {useNavigate} from "react-router-dom";


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
    const[doneVoting , setDoneVoting] = useState(false)
    const[tx_hash , setTx] = useState("")
    const cookie = new Cookies()
    const jwt = cookie.get("voter_token")
    const navigator = useNavigate()
    useEffect(() => {
        if(jwt === undefined) {
            navigator("/voterLogin")
        }
       axios.get("http://localhost:8000/allCandidates").then(res => {if (res.status === 200){setCandidates(res.data.candidates); console.log(Candidates)}})
    },[navigator])

    function sendVote(id){
        console.log(jwt.toString())
        const form = new FormData()
        form.set("token_voter" , jwt.toString())
        form.set("id" , id)
        axios.post("http://localhost:8000/castVote" , form).then(res => {
            if(res.status === 200){
                cookie.remove("voter_token");
                setDoneVoting(true);
                setTx(res.data.hash);
            }
        })
    }

    if(doneVoting){
        return (
            <div>
            <Navigator />
            <Container id='voting-cont'>
                <h3> You have already voted! Check your vote transaction <a href={`https://sepolia.etherscan.io/tx/${tx_hash}`}>here</a></h3>
            </Container>
                </div>
        )
    }

    else {

        return (

            <div>
                <Navigator/>
                <Container id='voting-cont'>
                    {
                        Candidates.map((element, index) => {
                            return (
                                <div className='card2' key={index}>
                                    <img src={element.party_photo_url} alt="candidate symbol" className='card2-img'/>
                                    <div className='card2-content'>
                                        <p>{element.name}</p>
                                        <Button className="card2-vote-btn" variant="contained" sx={btn} id={element.id}
                                                onClick={e => sendVote(element.id)}>Vote</Button>
                                    </div>
                                </div>
                            )
                        })
                    }

                </Container>
            </div>
        )
    }
}