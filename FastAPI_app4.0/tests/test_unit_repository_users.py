import unittest
from unittest.mock import MagicMock, patch
from libgravatar import Gravatar
from src.entity.models import User
from src.schemas.user import UserSchema
from unittest.mock import MagicMock, AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.users import get_user_by_email, create_user, update_token, update_avatar_url, confirmed_email, new_password

class TestRepositoryUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self)->None:
        self.body = UserSchema(username="NameTest",email="ex@example.com",password="passss")
        self.session = AsyncMock(spec=AsyncSession)

    async def test_create_user(self):
        with patch.object(Gravatar, 'get_image', return_value="https://www.gravatar.com/avatar/test_image") as mock_get_image:
            result = await create_user(self.body, self.session)
            mock_get_image.assert_called_once_with()
            self.assertIsInstance(result, User)
            self.assertEqual(result.username, self.body.username)
            self.assertEqual(result.email, self.body.email)
            self.assertEqual(result.password, self.body.password)
            self.assertEqual(result.avatar, "https://www.gravatar.com/avatar/test_image")
            self.assertTrue(hasattr(result, 'id'))

            self.session.add.assert_called_once_with(result)
            self.session.commit.assert_called_once()
            self.session.refresh.assert_called_once_with(result)
    
    async def test_get_user_by_email(self):
        user = User(email="test@ex.com", password="pass")
        mocked_user = Mock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(email="test@ex.com", db=self.session)
        self.assertEqual(result, user)

    async def test_update_token(self):
        user = User(email="test@ex.com", password="pass")
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_token(user, "new_token", self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(user.refresh_token, "new_token")
        self.assertIsNone(result)

    async def test_update_avatar_url(self):
        user = User(email="test@ex.com", password="pass")
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_avatar_url(user.email, "new_url_avatar", self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(user, result)
        self.assertIsInstance(result, User)
    
    async def test_confirmed_email(self):
        user = User(email="test@ex.com", password="pass")
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await confirmed_email(user.email, self.session)
        self.session.commit.assert_called_once()
        self.assertTrue(user.confirmed)
        self.assertIsNone(result)

    async def test_new_password(self):
        user = User(email="test@ex.com", password="pass")
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await new_password(user.email, "new_password", self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(user, result)
        self.assertIsInstance(result, User)
