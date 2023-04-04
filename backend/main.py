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
app.add_middleware(CORSMiddleware , allow_origins = ["http://localhost:8080"] , allow_credentials = True , allow_headers = ['*'] , allow_methods = ['*'])
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES_VOTER = 5
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN = 30
blockchain_url = "http://localhost:8545"
web3 = Web3(Web3.HTTPProvider(blockchain_url))
faucet_key = os.getenv("faucet_key")
faucet_addr = os.getenv("faucet_addr")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




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
def login_for_access_token(
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


def transferEth(wallet : str , value : float , email : str):
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
def create_user(first_name : str = Form(...) , last_name : str =  Form(...) , year : int = Form(...) , month : int = Form(...) , day : int = Form(...) , aadhaar : int = Form(...) , email : str = Form(...)):
    if checkAadhaarUsed(aadhaar):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    """Password is first four letter of first name in upper case + dob in format yyyymmdd
    Example : Voter with name Rahul Mishra born on 20/07/1995 will have password RAHU19950720
    """

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
    create_user_db(UserForm(first_name = first_name , last_name = last_name , email = email , year = year , month = month , day = day , aadhaar = aadhaar , disabled = True , password = hashed , wallet = wallet , private_key = private_key))
    return status.HTTP_201_CREATED

@app.post("/createAdmin")
def create_admin(email : str = Form(...) , password : str = Form(...) , wallet : str = Form(...) , private_key : str = Form(...)):
    hashed = get_password_hash(password)
    create_admin_db(AdminForm(email = email , password = hashed , wallet = wallet , private_key = private_key))
    return status.HTTP_201_CREATED


def authenticate_admin(email : str , password : str):
    admin = get_admin_details(email)
    if not admin :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin doesnt exist"
        )
    if not verify_password(password , admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password"
        )
    return admin
@app.post("/tokenAdmin" , response_model=Token)
def login_for_admin_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    admin = authenticate_admin(form_data.username , form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN)
    access_token = create_access_token(
        data={"sub": admin.email, "type": "admin"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/verifyVoter")
def verify_voter(aadhaar : int = Form(...) , token_admin : str =  Form(...)):
    payload = jwt.decode(token_admin , SECRET_KEY , algorithms=[ALGORITHM])
    if payload.get("type") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can verify voters"
        )
    if not checkAadhaarUsed(aadhaar):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voter not found in database"
        )
    set_voter_eligible(aadhaar)
    user = get_user_details(aadhaar)
    if web3.from_wei(web3.eth.get_balance(user.wallet) , "ether") < 0.001:
        transferEth(user.wallet , 0.001)