from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import contact as repo_contacts
from src.schemas.contact import ContactResponse, ContactSchema, ContactUpdateSchema
from src.services.auth import auth_service
from src.entity.models import User, Role
from src.services.roles import RoleAccess
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=['contacts'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])

# this is used to get all contacts - for user
@router.get("/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db), current_user:User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts.
    
    :param limit: int: Limit the number of contacts returned
    :param ge: Specify a minimum value for the limit parameter
    :param le: Limit the number of contacts returned to 500
    :param offset: int: Specify the number of records to skip
    :param ge: Specify the minimum value of limit
    :param db: AsyncSession: Get the database session
    :param current_user:User: Get the current user from the database
    :return: A list of contacts
    """
    contacts = await repo_contacts.get_contacts(limit, offset, db, current_user)
    return contacts

#this function is used to get all contacts
@router.get("/all", response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                        db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The get_all_contacts function returns a list of contacts.
        The limit and offset parameters are used to paginate the results.
        
    
    :param limit: int: Limit the number of contacts returned
    :param ge: Specify the minimum value of the parameter
    :param le: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before returning results
    :param ge: Specify the minimum value for a parameter
    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user from the database
    :return: A list of contacts
    """
    contacts = await repo_contacts.get_all_contacts(limit, offset, db) #TODO create funtion
    return contacts


# this is used to get birthdays of your contacts in 7 days
@router.get("/birthdays", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_birthday(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                                 db: AsyncSession = Depends(get_db), current_user:User = Depends(auth_service.get_current_user)):
    """
    The get_contacts_birthday function returns a list of contacts that have birthdays in the current month.
        The limit and offset parameters are used to paginate the results.
    
    
    :param limit: int: Limit the number of contacts returned
    :param ge: Set a minimum value for the limit parameter
    :param le: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param ge: Specify a minimum value for the parameter
    :param db: AsyncSession: Get the database session
    :param current_user:User: Get the current user from the database
    :return: A list of contacts that have a birthday today
    """
    contacts = await repo_contacts.get_contacts_birthday(limit, offset, db, current_user)
    return contacts

# this is used to get only 1 contact by the id
@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), 
                      current_user:User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    If no such contact exists, it will return a 404 error.
    
    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Get the database connection
    :param current_user:User: Get the user id of the current user
    :return: A contact object
    """
    contact = await repo_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

# this is used to create one new contact
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db), current_user:User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        It takes a ContactSchema object as input, and returns the newly created contact.
    
    :param body: ContactSchema: Validate the request body, and to convert it into a contact object
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user:User: Get the current user from the auth_service
    :return: The created contact
    """
    contact = await repo_contacts.create_contact(body, db, current_user)
    return contact

# this is used to update existed contact
@router.put("/{contact_id}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), 
                         current_user:User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        It takes an id, body and db as parameters. The id is used to find the contact in the database, 
        while body contains all of the information that will be updated for that contact. 
        If no such contact exists then it returns a 404 error.
    
    :param body: ContactUpdateSchema: Validate the body of the request
    :param contact_id: int: Identify the contact to be deleted
    :param db: AsyncSession: Get the database session
    :param current_user:User: Get the user who is making the request
    :return: A contact object
    """
    contact = await repo_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

# this is used to delete existed contact by the id
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                        current_user:User = Depends(auth_service.get_current_user) ):
    """
    The delete_contact function deletes a contact from the database.
        The function takes in an integer representing the id of the contact to be deleted, and returns a dictionary containing information about that contact.
    
    :param contact_id: int: Specify the contact_id of the contact to be deleted
    :param db: AsyncSession: Get the database session
    :param current_user:User: Get the current user from the auth_service
    :return: The contact that was deleted
    """
    contact = await repo_contacts.delete_contact(contact_id, db, current_user)
    return contact

# this is used to get existed contact by the name, last_name or(and) email
@router.get("/selected_contacts/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_select(
    name: str = Query(None, description="Search by name"),
    last_name: str = Query(None, description="Search by last name"),
    email: str = Query(None, description="Search by email"),
    limit: int = Query(10, ge=10, le=500), 
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user:User = Depends(auth_service.get_current_user)
):
    """
    The get_contacts_select function is used to search for contacts by name, last_name or email.
        The function returns a list of contacts that match the search criteria.
    
    :param name: str: Search by name
    :param description: Add a description to the parameter
    :param last_name: str: Search by last name, the limit: int parameter is used to set a limit of 10 contacts per page and the offset: int parameter is used to set an offset of 0
    :param description: Document the endpoint
    :param email: str: Search by email
    :param description: Provide a description of the endpoint in the openapi documentation
    :param limit: int: Limit the number of results returned
    :param ge: Check if the value is greater or equal to the value specified
    :param le: Limit the number of results that can be returned
    :param offset: int: Set the offset of the query
    :param ge: Validate that the value is greater than or equal to a given number
    :param db: AsyncSession: Get the database connection
    :param current_user:User: Validate that the user is logged in
    :return: A list of contacts
    """
    contacts_get = await repo_contacts.get_contacts_select(name, last_name, email, limit, offset, db, current_user)
    return contacts_get

