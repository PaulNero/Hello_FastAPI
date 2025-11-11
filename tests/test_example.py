import pytest
from sqlalchemy import select
from app.db.models import User

@pytest.mark.asyncio # Маркер асинхронного теста
async def test_create_user(async_session):
    # Создаём тестового пользователя
    new_user = User(username='John', email='test@test.test')
    async_session.add(new_user)
    await async_session.commit()
    assert new_user.id is not None
    
    # Проверяем в базе
    stmt = select(User).where(User.email == 'test@test.test')
    result = await async_session.execute(stmt)
    user_from_db = result.scalar_one()
    assert user_from_db.name == 'John' 