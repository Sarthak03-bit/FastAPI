from fastapi import APIRouter, Depends, HTTPException  , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from datetime import timedelta
import jwt


from models import UserPublic,UserInDB,UserBase,UserCreate, Token
from database import get_async_db
from database_models import User
from security import get_hased_password, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY,ALGORITHM


api =  APIRouter(prefix="/auth", tags=['auth'])

oauth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")



async def get_user_by_username(db : AsyncSession, username) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def authenticate_user(db : AsyncSession, user_name, password) -> User | None:
    user = await get_user_by_username(db , user_name)
    if user:
        if verify_password(password, user.hashed_password):
            return user
    
@api.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_new_user(user_in : UserCreate, db = Depends(get_async_db)):

    user = await get_user_by_username(db, user_in.username)
    if user:
        raise HTTPException(status = status.HTTP_409_CONFLICT, detail="User already exists, please login")
    
    hashed_pass = get_hased_password(user_in.password)
    new_user = User(
        username = user_in.username,
        email = user_in.email,
        hashed_password = hashed_pass
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@api.post("/token",response_model=Token)
async def login_for_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : AsyncSession = Depends(get_async_db)):
    user = await authenticate_user(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "Incorrect username or password")

    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token( data={"sub": user.username},expires_delta= access_token_expires)
    return Token(access_token=token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)] , db:AsyncSession = Depends(get_async_db) ):
    try:
        payload = jwt.decode(token,SECRET_KEY, ALGORITHM )
        username = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@api.get("/me", response_model=UserPublic)
async def read_user_me(current_user :Annotated[User, Depends(get_current_active_user)]):
    return current_user
