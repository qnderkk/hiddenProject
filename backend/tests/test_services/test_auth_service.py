import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin


@pytest.fixture
def user_repo_mock():
    return MagicMock()


@pytest.fixture
def auth_service(user_repo_mock):
    return AuthService(user_repo_mock)


@pytest.mark.asyncio
async def test_register_user_success(auth_service, user_repo_mock):
    # Настраиваем мок: пользователя с таким email нет
    user_repo_mock.get_by_email = AsyncMock(return_value=None)
    user_repo_mock.create = AsyncMock(return_value=MagicMock(id=1, email="test@test.com"))

    user_data = UserCreate(name="Test", email="test@test.com", password="password123")
    result = await auth_service.register_user(user_data)

    assert result is not None
    user_repo_mock.create.assert_called_once()
    # Проверяем, что пароль захеширован (не передается в открытом виде)
    args, kwargs = user_repo_mock.create.call_args
    assert args[1] != "password123"


@pytest.mark.asyncio
async def test_register_user_already_exists(auth_service, user_repo_mock):
    # Имитируем, что пользователь найден
    user_repo_mock.get_by_email = AsyncMock(return_value=MagicMock())

    user_data = UserCreate(name="Test", email="exists@test.com", password="123")
    result = await auth_service.register_user(user_data)

    assert result is None
    user_repo_mock.create.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(auth_service, user_repo_mock):
    hashed_password = auth_service.hash_password("correct_pass")
    mock_user = MagicMock(hashed_password=hashed_password)
    user_repo_mock.get_by_email = AsyncMock(return_value=mock_user)

    login_data = UserLogin(email="test@test.com", password="wrong_password")
    result = await auth_service.authenticate_user(login_data)

    # Меняем None на False, так как сервис возвращает False при ошибке пароля
    assert result is False