from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.src.users.models import User
from backend.src.users.schemas import UserRegistrationSchema


async def get(*, db_session: AsyncSession, user_id: int) -> User | None:
    """Returns a user based on the given user id."""
    result = await db_session.execute(select(User).filter(User.id == user_id))
    return result.scalars().one_or_none()


async def get_by_email(*, db_session: AsyncSession, email: str) -> User | None:
    """Returns a user object based on user email."""
    result = await db_session.execute(select(User).filter(User.email == email))
    return result.scalars().one_or_none()


async def create(*, db_session: AsyncSession, data: UserRegistrationSchema) -> User | None:
    """Create new user instance in db."""
    user = User(email=data.email, password=data.password, is_active=data.is_active)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
