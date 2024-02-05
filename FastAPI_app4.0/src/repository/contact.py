from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema

# this is used to get all contacts per User
async def get_contacts(limit: int, offset: int, db: AsyncSession, user:User):
    """
    The get_contacts function returns a list of contacts for the user.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before returning
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Filter the contacts by user
    :return: A list of contacts
    """
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

# this is used to get all contacts
async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_contacts function returns a list of all contacts in the database.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass the database connection to the function
    :return: A list of contact objects
    """
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

# this is used to get only 1 contact by the id
async def get_contact(contact_id: int, db: AsyncSession, user:User):
    """
    The get_contact function is used to retrieve a contact from the database.
    It takes in an integer representing the id of the contact, and returns a Contact object.
    If no such contact exists, it will return None.
    
    :param contact_id: int: Filter the contact by id
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Ensure that the user requesting the contact is the owner of it
    :return: A single contact
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

# this is used to create one new contact
async def create_contact(body: ContactSchema, db: AsyncSession, user:User):
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Connect to the database
    :param user:User: Get the user id from the token
    :return: A contact object
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

# this is used to update existed contact
async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user:User):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactUpdateSchema): A schema containing all fields that can be updated for a Contact object.  This is used to validate and deserialize the request body into an object that can be passed into this function as an argument.  See ContactUpdateSchema for more details on what fields are required/optional, etc...
    
    :param contact_id: int: Specify the contact we want to delete
    :param body: ContactUpdateSchema: Get the data from the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Identify the user who is making the request
    :return: The contact object that was updated
    """
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
    """
    The delete_contact function deletes a contact from the database.
        
    
    :param contact_id: int: Identify the contact to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Check if the user is allowed to delete the contact
    :return: The contact that was deleted
    """
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
    """
    The get_contacts_select function is used to retrieve contacts from the database.
    It takes in a name, last_name, email, limit and offset as parameters. The function then uses these parameters to create a select statement that will be executed by the database session object passed into it. If any of the optional parameters are not provided they will be ignored when creating this select statement.
    
    :param name: str: Filter the contacts by name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :param limit: int: Limit the number of results returned
    :param offset: int: Specify the offset of the first row to return
    :param db: AsyncSession: Pass the database connection to the function
    :param user:User: Filter the contacts by user
    :return: A list of contacts
    """
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
    """
    The get_contacts_birthday function returns a list of contacts with birthdays in the next 7 days.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Filter the contacts by user
    :return: A list of contacts with birthdays in the next 7 days
    """
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
    stmt = stmt.offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()