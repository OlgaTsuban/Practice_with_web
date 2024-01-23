from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema

# this is used to get all contacts per User
async def get_contacts(limit: int, offset: int, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

# this is used to get all contacts
async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

# this is used to get only 1 contact by the id
async def get_contact(contact_id: int, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

# this is used to create one new contact
async def create_contact(body: ContactSchema, db: AsyncSession, user:User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

# this is used to update existed contact
async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.additional_data = body.additional_data
        await db.commit()
        await db.refresh(contact)
    return contact

# this is used to delete existed contact by the id
async def delete_contact(contact_id: int, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact

# this is used to get existed contact by the name, last_name or(and) email
async def get_contacts_select(name: str, last_name: str, email: str,
                              limit: int, offset: int, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(user=user)
    if name:
        stmt = stmt.filter(Contact.first_name.ilike(f'%{name}%'))
    if last_name:
        stmt = stmt.filter(Contact.last_name.ilike(f'%{last_name}%'))
    if email:
        stmt = stmt.filter(Contact.email.ilike(f'%{email}%'))
    stmt = stmt.offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

# this is used to get birthdays of your contacts in 7 days
async def get_contacts_birthday(limit: int, offset: int, db: AsyncSession, user:User):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    # Query contacts with birthdays in the next 7 days
    stmt = (
        select(Contact)
        .filter(
            and_(
                func.to_char(Contact.birth_date, 'MM-DD') >= today.strftime("%m-%d"),
                func.to_char(Contact.birth_date, 'MM-DD') <= end_date.strftime("%m-%d")
            )
        )
        .filter_by(user=user)
    )
    # stmt = (
    #     select(Contact)
    #     .filter(Contact.birth_date.between(today, end_date))
    #     .filter_by(user=user)
    # )
    stmt = stmt.offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()