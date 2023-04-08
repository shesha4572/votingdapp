import Button from "@mui/material/Button"
import Symbol from "../images/candidate-sym-1.jpg";

const btn = {
    fontSize : '1.5rem',
    color : '#f0f7ff',
    backgroundColor:'#2B9D82FF',
    '&:hover' : {
        backgroundColor: '#217964'
    }
}

export const Card = () => {
    return(
        <div className='card2'>
            <img src={Symbol} alt="candidate symbol" className='card2-img'/>
            <Button className="card2-vote-btn" variant="contained" sx={btn}>Vote</Button>
        </div>
    )
}