from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import verify_password, get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserCreateInDB
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> User:
        filters = {
            "email":(email, "=")
        }
        user = await crud_user.search(db=db, filters=filters, single_result=True)
        if not user:
            return None
        if not verify_password(password, user.passwordHash):
            return None
        return user

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        user_data = obj_in.dict(exclude={"password_confirm"})
        hashed_password = get_password_hash(user_data.pop("password"))
        user_in_db = UserCreateInDB(
            **user_data,
            passwordHash=hashed_password,
            role=UserRole.INDIVIDUAL_USER
        )
        return await super().create(db=db, obj_in=user_in_db)

crud_user = CRUDUser(User, use_logical_delete=True)
