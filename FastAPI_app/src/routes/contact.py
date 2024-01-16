from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import contact as repo_contacts
from src.schemas.contact import ContactResponse, ContactSchema, ContactUpdateSchema

router = APIRouter(prefix='/contacts', tags=['contacts'])

# this is used to get all contacts
@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    contacts = await repo_contacts.get_contacts(limit, offset, db)
    return contacts

# this is used to get birthdays of your contacts in 7 days
@router.get("/birthdays", response_model=list[ContactResponse])
async def get_contacts_birthday(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                                 db: AsyncSession = Depends(get_db)):
    contacts = await repo_contacts.get_contacts_birthday(limit, offset, db)
    return contacts

# this is used to get only 1 contact by the id
@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

# this is used to create one new contact
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.create_contact(body, db)
    return contact

# this is used to update existed contact
@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

# this is used to delete existed contact by the id
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repo_contacts.delete_contact(contact_id, db)
    return contact

# this is used to get existed contact by the name, last_name or(and) email
@router.get("/selected_contacts/", response_model=list[ContactResponse])
async def get_contacts_select(
    name: str = Query(None, description="Search by name"),
    last_name: str = Query(None, description="Search by last name"),
    email: str = Query(None, description="Search by email"),
    limit: int = Query(10, ge=10, le=500), 
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    contacts_get = await repo_contacts.get_contacts_select(name, last_name, email, limit, offset, db)
    return contacts_get

