import Button from "@mui/material/Button";
import Symbol from "../images/candidate-sym-1.jpg"

const btn = {
    fontSize : '1.5rem',
    color : '#f0f7ff',
    backgroundColor:'#2B9D82FF',
    '&:hover' : {
        backgroundColor: '#217964'
    }
}

export const CardBig = () => {
    return(
        <div className='card'>
            <img src={Symbol} alt="candidate symbol" className='card-img'/>
            <div className='card-details'>
                <p>Candidate Name:</p>
                <p>Political Party:</p>
                <p>Age:</p>
                <p>Qualification:</p>
            </div>
            <Button className="card-vote-btn" variant="contained" sx={btn}>Vote</Button>
        </div>
    )
}