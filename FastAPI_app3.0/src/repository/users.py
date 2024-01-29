from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserSchema
from libgravatar import Gravatar

# Using the function get user by his/her email
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    statement = select(User).filter_by(email=email)
    user = await db.execute(statement)
    user = user.scalar_one_or_none()
    return user

# Create the user in DB
async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user) 
    return new_user

# Update the refresh token
async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()

# Comfirm the email of the user
async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

# Update the user's avatar  
async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


# Comfirm the email of the user
async def new_password(email: str, new_password:str, db: AsyncSession= Depends(get_db)):
    user = await get_user_by_email(email, db)
    user.password = new_password
    # user = User(**user.model_dump())
    # db.update(user)
    await db.commit()
    await db.refresh(user)
    return user