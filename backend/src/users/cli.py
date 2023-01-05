import typer as typer
from pydantic import EmailError, EmailStr
from rich import print

from backend.common.async_utils import async_to_sync
from backend.src.auth.security import get_password_hash
from backend.src.dashboard import services as dashboard_service
from backend.src.database.core import async_session, engine
from backend.src.users import services as user_service
from backend.src.users.schemas import UserRegistrationSchema, UserSchema

app = typer.Typer()


@async_to_sync
async def _validate_email(value: str) -> str:
    try:
        EmailStr.validate(value)
    except EmailError as exc:
        raise typer.BadParameter(exc.msg_template)

    async with async_session() as session:
        if await user_service.get_by_email(db_session=session, email=value):
            raise typer.BadParameter(f"User with email {value} already exists")
    await engine.dispose()

    return value


def _validate_password(value: str) -> str:
    if len(value) < 8:
        raise typer.BadParameter("Your password must contain at least 8 characters")
    return value


@app.command("create")
@async_to_sync
async def create(
    email: str = typer.Option(..., prompt=True, callback=_validate_email),
    first_name: str = typer.Option(..., prompt=True, min=1, max=20),
    last_name: str = typer.Option(..., prompt=True, min=1, max=20),
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True, callback=_validate_password
    ),
) -> None:
    """Create new user."""

    data = UserRegistrationSchema(
        email=email,
        password=get_password_hash(password),
        is_active=True,
        first_name=first_name,
        last_name=last_name,
    )
    async with async_session() as session:
        user = await user_service.create(db_session=session, data=data)
        if user:
            await dashboard_service.create(db_session=session, user_id=user.id)
            await session.commit()
            await session.refresh(user)

    print("New user successfully created! :tada:")
    print(UserSchema.from_orm(user).dict())
