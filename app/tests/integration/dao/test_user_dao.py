from app.dao.user import UserDAO
from app.models.user import User


class TestUserDAO:
    async def test_user_dao_add(self, get_test_db):
        adding_response = await UserDAO.add(
            get_test_db,
            email="jHkV8@example.com",
            hashed_password="$2b$12$iJGPfVq2f7nXXOcuCMYd.OOZGfjGw5svQjWeyZ81l4fVATZNnw0LW",
        )
        assert adding_response == "User has been created"

    async def test_user_is_superuser(self, get_test_db):
        user = await UserDAO.find_by_id(get_test_db, 1)
        assert isinstance(user, User)

        is_superuser = await UserDAO.is_super_user(user)
        assert is_superuser is True

    async def test_user_auth(self, get_test_db):
        user = await UserDAO.authenticate_user(
            get_test_db, email="jHkV8@example.com", password="password"
        )
        assert isinstance(user, User)

    async def test_user_dao_find_all(self, get_test_db):
        users = await UserDAO.find_all(get_test_db)
        assert isinstance(users, list)
        assert len(users) > 0

    async def test_user_dao_update(self, get_test_db):
        updated_response = await UserDAO.update(get_test_db, 2, is_superuser=True)
        assert updated_response == "User with id 2 has been updated"

        updated_user = await UserDAO.find_by_id(get_test_db, 2)
        is_superuser = await UserDAO.is_super_user(updated_user)
        assert is_superuser is True

    async def test_user_delete(self, get_test_db):
        deleted_response = await UserDAO.delete_by_id(get_test_db, 2)
        assert deleted_response == "User with id 2 has been deleted"

        deleted_user = await UserDAO.find_by_id(get_test_db, 2)
        assert deleted_user is None
