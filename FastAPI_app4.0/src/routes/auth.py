from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import users as repo_users
from src.schemas.user import UserSchema, TokenSchema, UserResponse, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email, send_email_reset_password
from starlette.responses import JSONResponse
from src.conf import messages
router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()

# Use for signup
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, bt:BackgroundTasks,request: Request, db: AsyncSession = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes a UserSchema object as input, and returns the newly created user.
        If an account with that email already exists, it raises an HTTPException.
    
    :param body: UserSchema: Validate the request body
    :param bt:BackgroundTasks: Add a task to the background queue
    :param request: Request: Get the base_url of the application
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object
    """
    exist_user = await repo_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXIST)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repo_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user

# Use for login
@router.post("/login",  response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes in the email and password of the user, verifies that they are correct,
        and then returns an access token for future requests.
    
    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: AsyncSession: Pass the database session to the function
    :return: A dictionary with the access token, refresh token and the type of token
    """
    user = await repo_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL) # sometimes it is better to hide error
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_CONFIRMED)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD) # sometimes it is better to hide error
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repo_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Use for get a refresh token
@router.get('/refresh_token',  response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                        db: AsyncSession = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access_token, 
        a new refresh_token, and the type of token (bearer).
    
    :param credentials: HTTPAuthorizationCredentials: Get the access token from the header
    :param db: AsyncSession: Get the database session
    :return: A new access token and a new refresh token
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repo_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repo_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_REF_TOKEN)

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repo_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Use for confirm your email
@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    The confirmed_email function is used to confirm the user's email address.
        It takes a token as an argument and returns a message if the email has been confirmed or not.
    
    :param token: str: Get the token from the url
    :param db: AsyncSession: Pass the database session to the function
    :return: A dictionary with the message key and a string value
    """
    email = await auth_service.get_email_from_token(token)
    user = await repo_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repo_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

# Use for email for confirm password
@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link that will confirm their account.
        The function takes in a RequestEmail object, which contains the user's email address. It then checks if the 
        user exists and if they have already confirmed their account. If they haven't, it sends them an email with a 
        confirmation link.
    
    :param body: RequestEmail: Pass the email address to the function
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the server
    :param db: AsyncSession: Get a database session from the dependency
    :return: A message to the user, which will be displayed on the frontend
    """
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
    """
    The forget_password function is used to send an email to the user with a link
    to reset their password. The function takes in the RequestEmail schema, which contains
    the email of the user who wants to reset their password. It then checks if that email exists in our database, and if it does not exist, we return a 500 error code with an appropriate message. If it does exist however, we call our background task function send_email_reset_password and pass in the users' username and base url as parameters.
    
    :param fpr: RequestEmail: Get the email address from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks
    :param request: Request: Get the base url of the request
    :param db: AsyncSession: Get the database connection
    :return: A jsonresponse object
    """
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
    """
    The reset_password function takes a token and new password as input,
        then checks if the user exists in the database. If they do exist,
        it will update their password to the new one provided.
    
    :param token: str: Get the email from the token
    :param new_password: str: Get the new password from the user
    :param db: AsyncSession: Get the database connection
    :return: A message if the user's email is not confirmed
    """
    email = await auth_service.get_email_from_token(token)
    user = await repo_users.get_user_by_email(email, db)
    password = auth_service.get_password_hash(new_password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if not user.confirmed:
        return {"message": "Your email is not confirmed "}
    await repo_users.new_password(user.email, password, db)
    return {"message": "Password changed"}

# Use for getting a token for using method POST
@router.get('/reset_password/{token}') 
async def get_user_by_reset_token(token: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_reset_token function is used to get a user by their reset token.
        This function will return the user's email address if they have a valid reset token.
    
    :param token: str: Get the email from the token
    :param db: AsyncSession: Pass in the database session to the function
    :return: A dictionary with the token
    """
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
