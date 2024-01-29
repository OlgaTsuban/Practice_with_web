from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import users as repo_users
from src.schemas.user import UserSchema, TokenSchema, UserResponse, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email, send_email_reset_password
from starlette.responses import JSONResponse

router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()

# Use for signup
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, bt:BackgroundTasks,request: Request, db: AsyncSession = Depends(get_db)):
    exist_user = await repo_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repo_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user

# Use for login
@router.post("/login",  response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await repo_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email") # sometimes it is better to hide error
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password") # sometimes it is better to hide error
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repo_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Use for get a refresh token
@router.get('/refresh_token',  response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                        db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repo_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repo_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repo_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Use for confirm your email
@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await repo_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repo_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

# Use for email for confirm password
@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    user = await repo_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}

# Use for getting email about token for token to reset old password
@router.post("/forget-password")
async def forget_password(
    fpr: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await repo_users.get_user_by_email(fpr.email, db)
        if user is None:
           raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail="Invalid Email address")
        background_tasks.add_task(send_email_reset_password, user.email, user.username, str(request.base_url))
        return JSONResponse(status_code=status.HTTP_200_OK,
           content={"message": "Email has been sent", "success": True,
               "status_code": status.HTTP_200_OK})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail="Something Unexpected, Server Error")
    
# Use for reset old password after getting the email
@router.post('/reset_password/{token}') 
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await repo_users.get_user_by_email(email, db)
    password = auth_service.get_password_hash(new_password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if not user.confirmed:
        return {"message": "Your email is not confirmed "}
    await repo_users.new_password(user.email, password, db)
    return {"message": "Password changed"}

# Use for getting a token for use method POST
@router.get('/reset_password/{token}') 
async def get_user_by_reset_token(token: str, db: AsyncSession = Depends(get_db)):
    try:
        # print(token)
        email = await auth_service.get_email_from_token(token)
        user = await repo_users.get_user_by_email(email, db)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
        
        if not user.confirmed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your email is not confirmed")
        return {f"Token": {token}}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
