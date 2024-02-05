import unittest
from datetime import date
from unittest.mock import MagicMock, AsyncMock, Mock, ANY
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema
from src.repository.contact import create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_contacts, get_contacts_select, get_contacts_birthday
from sqlalchemy import select

class TestAsyncContact(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='test_title_1',last_name='test_title_1', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 5, 13),  
                            additional_data='test_description_1', user=self.user),
                    Contact(id=2, first_name='test_title_2',last_name='test_title_2',email='ex2@gmail.com',
                            phone_number="+380689999233", birth_date=date(1995, 7, 13),  
                            additional_data='test_description_2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='test_title_1',last_name='test_title_1', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 5, 13),  
                            additional_data='test_description_1', user=self.user),
                Contact(id=2, first_name='test_title_2',last_name='test_title_2',email='ex2@gmail.com',
                            phone_number="+380689999233", birth_date=date(1995, 7, 13),  
                            additional_data='test_description_2', user=self.user)]
        mocked_contacts = Mock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactSchema(first_name='test_title_1',last_name='test_title_1', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 5, 13))
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.email, body.email)

    async def test_update_contact(self):
        body = ContactUpdateSchema(first_name='test_title_01',last_name='test_title_01', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 1, 13))
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name='test_title_01',last_name='test_title_01', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 1, 13))
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.email, body.email)

    async def test_delete_contact(self):
        mocked_todo = MagicMock()
        mocked_todo.scalar_one_or_none.return_value = Contact(id=1, first_name='test_title_01',last_name='test_title_01', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 1, 13),
                                                           user=self.user)
        self.session.execute.return_value = mocked_todo
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_get_contact(self):
        contact = Contact(id=1, first_name='test_title_1',last_name='test_title_1', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 5, 13),  
                            additional_data='test_description_1', user=self.user)
        mocked_contacts = Mock()
        mocked_contacts.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contacts
        result = await get_contact(contact_id=1, db=self.session, user=self.user)
        self.assertEqual(result, contact)

    async def test_get_contacts_birthday(self):
        limit = 10
        offset = 0
        # today = datetime.now().date()
        contacts = [Contact(id=1, first_name='test_title_1',last_name='test_title_1', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 2, 13),  
                            additional_data='test_description_1', user=self.user),
                    Contact(id=2, first_name='test_title_2',last_name='test_title_2',email='ex2@gmail.com',
                            phone_number="+380689999233", birth_date=date(1995, 2, 1),  
                            additional_data='test_description_2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts_birthday(limit, offset, self.session, self.user)
        # expected_query = (
        #     select(Contact)
        #     .filter(
        #         and_(
        #             func.to_char(Contact.birth_date, 'MM-DD') >= today.strftime("%m-%d"),
        #             func.to_char(Contact.birth_date, 'MM-DD') <= (today + timedelta(days=7)).strftime("%m-%d")
        #         )
        #     )
        #     .filter_by(user=self.user)
        #     .offset(offset).limit(limit)
        # )
        # print("------------------------------------")
        # print("Actual Query:", self.session.execute.call_args[0][0])
        # print("Expected Query:", expected_query)

        # self.session.execute.assert_called_once_with(str(expected_query))
        self.assertEqual(result, contacts)

    async def test_get_contacts_select(self):
        contacts = [Contact(id=1, first_name='test_title_1',last_name='test_title_1', email='ex@gmail.com', 
                            phone_number="+380689999222", birth_date=date(1995, 2, 13),  
                            additional_data='test_description_1', user=self.user),
                    Contact(id=2, first_name='test_title_2',last_name='test_title_2',email='ex2@gmail.com',
                            phone_number="+380689999233", birth_date=date(1995, 2, 1),  
                            additional_data='test_description_2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts_select(name='test_title_1', last_name='test_title_1', email='ex@gmail.com',
                                           limit=10, offset=0, db=self.session, user=self.user)
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # print(result)
        expected_query = (
        select(Contact)
        .filter_by(user=self.user)
        .filter(Contact.first_name.ilike('%test_title_1%'))
        .filter(Contact.last_name.ilike('%test_title_1%'))
        .filter(Contact.email.ilike('%ex@gmail.com%'))
        .offset(0)
        .limit(10)
        )
        self.session.execute.assert_called_once_with(ANY)  # Using ANY matcher for the expected argument
        actual_query = self.session.execute.call_args[0][0]

    # Ensure that the actual query is equivalent to the expected query
        self.assertEqual(str(actual_query), str(expected_query))
        self.assertEqual(result, contacts)
        