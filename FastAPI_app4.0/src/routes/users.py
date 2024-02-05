from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
)
from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repo_users
import cloudinary
import cloudinary.uploader
import pickle

router = APIRouter(prefix="/users", tags=["users"])

cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)

# Use for getting info about yourself
@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_me function returns the current user's information.
        ---
    get:
        description: Returns the current user's information.
        responses:  # The possible responses that can be returned by this function, and their status codes.  This is a helpful way to document what your API will return when called with different parameters or in different states of operation.   It also helps you think about how you want to handle errors and other exceptional cases!
    
    :param current_user: User: Specify that the function expects a user object
    :return: The current user
    """
    return current_user

# Use for setting new avatar
@router.patch("/avatar", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_avatar(file: UploadFile = File(), db: AsyncSession = Depends(get_db),
                        user: User = Depends(auth_service.get_current_user)):
    """
    The update_avatar function is used to update the avatar of a user.
    
    :param file: UploadFile: Get the file from the request
    :param db: AsyncSession: Get the database connection
    :param user: User: Get the user from the database
    :return: The user object with the updated avatar
    """
    public_id = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    #print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repo_users.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user


