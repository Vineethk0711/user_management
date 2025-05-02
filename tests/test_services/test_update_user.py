import unittest
from unittest.mock import AsyncMock, MagicMock
from app.services.user_service import UserService
from app.models.user_model import User
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from uuid import uuid4


async def test_update_user_success():
    # Mock session and query result
    session_mock = AsyncMock()
    # Create a mock user object with the initial email address
    initial_email = 'test@example.com'
    user_mock = User(id=uuid4(), email=initial_email)
    query_result_mock = MagicMock()
    query_result_mock.scalars.return_value.first.return_value = user_mock
    session_mock.execute.return_value = query_result_mock

    # Mock update data
    new_email = 'test@example.com'
    update_data = {'email': new_email}

    # Call the update method
    updated_user = await UserService.update(session_mock, uuid4(), update_data)

    # Assert that the update method returns the updated user
    assert isinstance(updated_user, User)
    assert updated_user.email == new_email  # Check if the email has been updated


async def test_update_user_validation_error():
    # Mock session and query result
    session_mock = AsyncMock()

    # Mock invalid update data
    invalid_update_data = {'email': 'invalid_email'}

    # Call the update method with invalid data
    updated_user = await UserService.update(session_mock, uuid4(), invalid_update_data)

    # Assert that the update method returns None due to validation error
    assert updated_user is None


async def test_update_user_database_error():
    # Mock session
    session_mock = AsyncMock()

    # Mock SQLAlchemy error
    session_mock.execute.side_effect = SQLAlchemyError()

    # Mock valid update data
    update_data = {'email': 'new_email@example.com'}

    # Call the update method
    updated_user = await UserService.update(session_mock, uuid4(), update_data)

    # Assert that the update method returns None due to database error
    assert updated_user is None


if __name__ == '__main__':
    unittest.main()
