from app.models.user import User, UserRole

from app.db.session import get_db
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_async_db():
    async_gen = get_db()
    db = await anext(async_gen)
    try:
        yield db
    finally:
        await db.close()


async def seed_data(db: AsyncSession):
    if db is None:
        raise ValueError("Database session is not available.")

    print("Seeding data...")

    data = [
        [
            User(
                username="admin",
                email="admin@gmail.com",
                phoneNumber="01234567890",
                passwordHash="$2b$12$d463yKk8JH8VkpNv6jglt.JnyU8PmA.lbFmYuHo9S2HOvdP3dA1oW",  # Sameh@123
                role=UserRole.SYSTEM_ADMIN.value,
                isActive=True,
            ),
            User(
                organizationId=1,
                username="user",
                email="orgAdmin@gmail.com",
                phoneNumber="01234567891",
                passwordHash="$2b$12$d463yKk8JH8VkpNv6jglt.JnyU8PmA.lbFmYuHo9S2HOvdP3dA1oW",  # Sameh@123
                role=UserRole.INDIVIDUAL_USER.value,
                isActive=True,
            ),
            User(
                username="user",
                email="orgUser@gmail.com",
                phoneNumber="01234567892",
                passwordHash="$2b$12$d463yKk8JH8VkpNv6jglt.JnyU8PmA.lbFmYuHo9S2HOvdP3dA1oW",  # Sameh@123
                role=UserRole.INDIVIDUAL_USER.value,
                isActive=True,
            ),
            User(
                username="user",
                email="user@gmail.com",
                phoneNumber="01234567893",
                passwordHash="$2b$12$d463yKk8JH8VkpNv6jglt.JnyU8PmA.lbFmYuHo9S2HOvdP3dA1oW",  # Moneeb@123
                role=UserRole.INDIVIDUAL_USER.value,
                isActive=True,
            ),
        ]
    ]

    for item in data:
        try:
            db.add_all(item)
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()


async def main():
    async with get_async_db() as db:
        await seed_data(db)


if __name__ == "__main__":
    asyncio.run(main())
