import logging
import asyncio

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy.future import select


@asynccontextmanager
async def get_async_db():
    async_gen = get_db()
    db = await anext(async_gen)
    try:
        yield db
    finally:
        await db.close()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init(db: AsyncSession) -> None:
    try:
        # Try to create session to check if DB is awake
        query = select(1)
        await db.execute(query)
    except Exception as e:
        logger.error(e)
        raise e


async def main():
    logger.info("Initializing service")
    async with get_async_db() as db:
        await init(db)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())