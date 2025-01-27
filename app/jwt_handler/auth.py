from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from app.exceptions.app_exceptions import CredentialsException

SECRET_KEY = "08f92b7cc3fbae22e3105fd7c866a862aee14fde178f51ac0cbb6cf02086d323"
ALGORITHM = "HS256"

TOKEN = None

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
outh2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    disabled: bool | None = None

credentials = {
    "naveen" : {
        "user_id": 1,
        "username" : "naveen",
        "hashed_password" : "$2b$12$SOBTr0VgpdT/aVSDfWyd8.MAS7m5IcXhuO/SImL8zxU3OQ3aDYaq2",
        "disabled": False
    }
}

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_user(credentials, username):
    if username in credentials:
        user = credentials[username]
        return User(**user)


def authenticate_user(credentials, username: str, password: str):
    user = get_user(credentials, username)
    if not user:
        return False
    if not verify_password(password, credentials[username]["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expiry: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expiry)
    expiring_time = int(expire.timestamp())
    to_encode.update({"exp": expiring_time})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    global TOKEN
    TOKEN = encode_jwt
    return encode_jwt

def get_current_active_user():
    try:
        if TOKEN == None:
            raise CredentialsException("Generate a token for the service")
        else:
            payload = jwt.decode(TOKEN, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except InvalidTokenError:
        raise CredentialsException("Time Limit Exceeded")