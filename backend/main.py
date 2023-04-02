from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta , date
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.database import *
from backend.models import *
from eth_account import Account
import secrets
from web3 import Web3


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8080"])
SECRET_KEY = "23e90f52049f07bb63d41c755cc41a337342762b26fd1ea5fbf7bd037c0b36c8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES_VOTER = 5
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN = 30
blockchain_url = "http://localhost:8545"
web3 = Web3(Web3.HTTPProvider(blockchain_url))
faucet_key = "0x50abd8b341979cee2812665b6e0ebd6f9985c6c4015e0d1d75db024f9cd5c516"
faucet_addr = "0x7892303D2e3523DcD3Edf0B11cea189AFD15ba0f"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()




def calculateAge(year , month , day):
    birthDate = date(year , month , day)
    today = date.today()
    age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(aadhaar: int):
    if not checkAadhaarUsed(aadhaar):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesnt exist"
        )
    user = get_user_details(aadhaar)
    return user


def authenticate_user(aadhaar: int, password: str):
    user : UserForm = get_user(aadhaar)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/tokenVoter", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):

    user = authenticate_user(int(form_data.username), form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES_VOTER)
    access_token = create_access_token(
        data={"sub": user.aadhaar , "type" : "voter" , "eligible" : not user.disabled}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def default():
    return {"res" : "Hello World"}


async def transferEth(wallet : str , value : float):
    nonce = web3.eth.get_transaction_count(faucet_addr)
    tx = {
        'nonce': nonce,
        'to': wallet,
        'value': web3.to_wei(value, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price
    }
    signed_tx = Account.sign_transaction(tx , faucet_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)


@app.post("/createVoter")
async def create_user(first_name : str = Form(...) , last_name : str =  Form(...) , year : int = Form(...) , month : int = Form(...) , day : int = Form(...) , aadhaar : int = Form(...) , email : str = Form(...)):
    if checkAadhaarUsed(aadhaar):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    password = first_name[:4].upper() + str(year) + ("0" + str(month) if month < 10 else str(month)) + ("0" + str(day) if day < 10 else str(day))
    hashed = get_password_hash(password)
    age = calculateAge(year , month , day)
    if age < 18:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Age is less than 18"
        )
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    wallet = Account.from_key(private_key).address
    #transferEth(wallet , 0.01)
    create_user_db(UserForm(first_name = first_name , last_name = last_name , email = email , year = year , month = month , day = day , aadhaar = aadhaar , disabled = True , password = hashed , wallet = wallet , private_key = private_key))
    return status.HTTP_201_CREATED

